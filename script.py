import platform
import uuid
import json
import tkinter as tk
from tkinter import messagebox
import os
import re
import subprocess

def get_hwid():
    system_info = platform.uname()
    mac = hex(uuid.getnode())
    hwid = f"{system_info.system}-{system_info.node}-{system_info.release}-{mac}"
    return hwid

def salvar_dados(email, senha):
    hwid = get_hwid()
    data = {
        "HWID": hwid,
        "Email": email,
        "Senha": senha,
    }
    
    try:
        with open("data.json", "w") as file:
            json.dump(data, file)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar data: {e}")

def salvar_config(config_data):
    try:
        with open("config.json", "w") as file:
            json.dump(config_data, file)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar configuração: {e}")

def read():
    if os.path.exists("data.json"):
        try:
            with open("data.json", "r") as file:
                return json.load(file)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao ler dados: {e}")
    return None

def read_config():
    if os.path.exists("config.json"):
        try:
            with open("config.json", "r") as file:
                return json.load(file)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao ler configuração: {e}")
    return {}

def on_submit():
    email = entry_email.get()
    senha = entry_senha.get()
    
    if not senha:
        messagebox.showwarning("Aviso", "A senha não pode estar vazia.")
        return
    
    if validar_email(email):
        salvar_dados(email, senha)
        criar_interface_config()  # Open config interface
        root.withdraw()  # Hide the login interface
    else:
        messagebox.showwarning("Aviso", "Email Inválido")

def open_relauncher():
    exe = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    if os.path.exists(exe):
        subprocess.run([exe])
    else:
        print(f"Erro: O arquivo {exe} não foi encontrado.")

def validar_email(email):
    padrao = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(padrao, email) is not None

def verificar_login():
    dados = read()
    if dados:
        current_hwid = get_hwid()
        if dados["HWID"] != current_hwid:
            messagebox.showwarning("HWID Mismatch", "O HWID deste computador não corresponde ao HWID salvo. Acesso negado.")
            return  # Exit the function if HWID doesn't match
        
        messagebox.showinfo("Bem-vindo", "Login bem-sucedido!")
        criar_interface_config()
        root.withdraw()  # Hide the login window
    else:
        criar_interface_login()

def criar_interface_login():
    global entry_email, entry_senha

    root.title("Login")
    root.geometry("200x130")
    centralizar_janela(root, 200, 130)

    label_email = tk.Label(root, text="Digite o Email:")
    label_email.pack()

    entry_email = tk.Entry(root)
    entry_email.pack()

    label_senha = tk.Label(root, text="Digite a Senha:")
    label_senha.pack()

    entry_senha = tk.Entry(root, show='*')
    entry_senha.pack()

    button_submit = tk.Button(root, text="Enviar", command=on_submit)
    button_submit.pack()

def criar_interface_config():
    config_window = tk.Toplevel(root)
    config_window.title("Configurações")
    config_window.geometry("300x200")
    centralizar_janela(config_window, 300, 200)

    tk.Label(config_window, text="Configurações:").pack()

    # Retrieve existing configuration
    config_data = read_config()

    # Add fields for configuration
    tk.Label(config_window, text="Config 1:").pack()
    entry_config1 = tk.Entry(config_window)
    entry_config1.pack()
    entry_config1.insert(0, config_data.get("Config1", ""))  # Pre-fill if exists

    tk.Label(config_window, text="Config 2:").pack()
    entry_config2 = tk.Entry(config_window)
    entry_config2.pack()
    entry_config2.insert(0, config_data.get("Config2", ""))  # Pre-fill if exists

    def auto_save_config(*args):
        config_data = {
            "Config1": entry_config1.get(),
            "Config2": entry_config2.get()
        }
        salvar_config(config_data)

    # Bind the auto-save function to changes in the entry fields
    entry_config1.bind("<KeyRelease>", auto_save_config)
    entry_config2.bind("<KeyRelease>", auto_save_config)

def centralizar_janela(janela, largura, altura):
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    pos_x = (largura_tela // 2) - (largura // 2)
    pos_y = (altura_tela // 2) - (altura // 2)
    
    janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

# Iniciar a aplicação
    
root = tk.Tk()
verificar_login()
root.mainloop()