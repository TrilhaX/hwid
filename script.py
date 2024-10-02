import sqlite3
import platform
import uuid
import json
import tkinter as tk
from tkinter import messagebox
import os
import re
import bcrypt
import subprocess

root = tk.Tk()

def get_hwid():
    system_info = platform.uname()
    mac = hex(uuid.getnode())
    hwid = f"{system_info.system}-{system_info.node}-{system_info.release}-{mac}"
    return hwid

def hash_password(password):
    # Gera um salt e hash a senha
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode(), stored_password.encode())

def create_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hwid TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

def add_hwid(hwid, email, password):
    password_hash = hash_password(password)
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (hwid, email, password) VALUES (?, ?, ?)', (hwid, email, password_hash))
        conn.commit()
    except sqlite3.IntegrityError:
        messagebox.showwarning("Warning", "Email is already registered.")
    finally:
        conn.close()

def verify_login(email, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM users WHERE email = ?', (email,))
    stored_password = cursor.fetchone()
    conn.close()

    if stored_password:
        return verify_password(stored_password[0], password)
    return False

def save_data(email, password):
    hwid = get_hwid()
    data = {
        "HWID": hwid,
        "Email": email,
        "Password": password,
        "SaveCredentials": save_credentials.get()
    }

    try:
        with open("account.json", "w") as file:
            json.dump(data, file)
    except Exception as e:
        messagebox.showerror("Error", f"Error saving data: {e}")

def read_data():
    if os.path.exists("account.json"):
        try:
            with open("account.json", "r") as file:
                data = json.load(file)
                if "SaveCredentials" not in data:
                    data["SaveCredentials"] = False
                return data
        except Exception as e:
            messagebox.showerror("Error", f"Error reading data: {e}")
    return None

def on_login_submit():
    email = entry_email.get()
    password = entry_password.get()

    if not password:
        messagebox.showwarning("Warning", "Password cannot be empty.")
        return

    if verify_login(email, password):
        if save_credentials.get():
            save_data(email, password)
        messagebox.showinfo("Welcome", "Login successful!")
        messagebox.showinfo("W.I.P", "Soon!")
    else:
        messagebox.showwarning("Warning", "Invalid email or password.")

def on_register_submit():
    email = entry_register_email.get()
    password = entry_register_password.get()
    
    if not password:
        messagebox.showwarning("Warning", "Password cannot be empty.")
        return

    if validate_email(email):
        add_hwid(get_hwid(), email, password)
        messagebox.showinfo("Success", "Registration successful!")
        register_window.destroy()
    else:
        messagebox.showwarning("Warning", "Invalid email.")

def validate_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

save_credentials = tk.BooleanVar()

def create_login_interface():
    global entry_email, entry_password

    root.title("Login")
    root.geometry("300x250")
    center_window(root, 300, 250)

    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg='black')

    tk.Label(root, text="Enter Email:", bg='black', fg='white').pack(pady=(5, 0))
    entry_email = tk.Entry(root, bg='darkgray', fg='white', bd=2, highlightbackground='white', highlightcolor='white')
    entry_email.pack(pady=(0, 5))

    tk.Label(root, text="Enter Password:", bg='black', fg='white').pack(pady=(5, 0))
    entry_password = tk.Entry(root, show='*', bg='darkgray', fg='white', bd=2, highlightbackground='white', highlightcolor='white')
    entry_password.pack(pady=(0, 10))

    tk.Checkbutton(root, text="Save credentials", variable=save_credentials, bg='gray', fg='black', selectcolor='white').pack(pady=(5, 10))

    button_login = tk.Button(root, text="Login", command=on_login_submit, bg='white', fg='black')
    button_login.pack(pady=(5, 10))

    button_register = tk.Button(root, text="Register", command=create_register_interface, bg='white', fg='black')
    button_register.pack(pady=(5, 20))

    saved_data = read_data()
    if saved_data:
        entry_email.insert(0, saved_data["Email"])
        entry_password.insert(0, saved_data["Password"])
        save_credentials.set(saved_data.get("SaveCredentials", False))

def create_register_interface():
    global entry_register_email, entry_register_password, register_window

    register_window = tk.Toplevel(root)
    register_window.title("Registration")
    register_window.geometry("300x200")
    center_window(register_window, 300, 200)

    register_window.configure(bg='black')

    tk.Label(register_window, text="Enter Email:", bg='black', fg='white').pack(pady=(5, 0))
    entry_register_email = tk.Entry(register_window, bg='darkgray', fg='white', bd=2, highlightbackground='white', highlightcolor='white')
    entry_register_email.pack(pady=(0, 5))

    tk.Label(register_window, text="Enter Password:", bg='black', fg='white').pack(pady=(5, 0))
    entry_register_password = tk.Entry(register_window, show='*', bg='darkgray', fg='white', bd=2, highlightbackground='white', highlightcolor='white')
    entry_register_password.pack(pady=(0, 10))

    button_register = tk.Button(register_window, text="Register", command=on_register_submit, bg='white', fg='black')
    button_register.pack(pady=(5, 20))

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    pos_x = (screen_width // 2) - (width // 2)
    pos_y = (screen_height // 2) - (height // 2)
    
    window.geometry(f"{width}x{height}+{pos_x}+{pos_y}")

create_database()
create_login_interface()
root.mainloop()