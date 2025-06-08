from db import execute_script
import tkinter as tk
from tkinter import ttk

from pages.livros_page import livros_page
from pages.usuarios_page import usuarios_page
from pages.funcionarios_page import funcionarios_page
from pages.emprestimos_page import emprestimos_page

def abrir_pagina(root, pagina_func):
    for widget in root.winfo_children():
        widget.destroy()
    pagina_func(root)

def abrir_em_nova_janela(pagina_func):
    nova_janela = tk.Toplevel()
    nova_janela.attributes('-fullscreen', True)
    nova_janela.configure(bg="#f5f7fa")
    pagina_func(nova_janela)
    nova_janela.bind('<Escape>', lambda e: nova_janela.destroy())

def menu_principal(root):
    for widget in root.winfo_children():
        widget.destroy()
    root.title("Sistema da Biblioteca")
    root.attributes('-fullscreen', True)
    root.configure(bg="#f5f7fa")
    
    # Estilo visual
    style = ttk.Style(root)
    style.theme_use('clam')

    style.configure('TButton',
        font=('Segoe UI', 14),
        padding=12,
        width=25,
        background='#3498db',
        foreground='white',
        relief='flat'
    )
    style.map('TButton',
        background=[('active', '#2980b9')],
        foreground=[('active', 'white')]
    )

    # Container Central
    container = ttk.Frame(root, padding=30)
    container.grid(row=0, column=0, sticky="nsew")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Título
    titulo = ttk.Label(container, text="📚 Biblioteca Virtual", font=("Segoe UI", 26, "bold"), anchor="center")
    titulo.grid(row=0, column=0, pady=(0, 40))

    # Botões de Acesso
    botoes = [
        (" Livros", livros_page),
        (" Usuários", usuarios_page),
        (" Funcionários", funcionarios_page),
        (" Empréstimos", emprestimos_page),
    ]

    for i, (texto, func) in enumerate(botoes):
        btn = ttk.Button(container, text=texto)
        btn.grid(row=i+1, column=0, pady=10)

        btn.bind("<Button-1>", lambda e, f=func: abrir_pagina(root, f))
        btn.bind("<Button-3>", lambda e, f=func: abrir_em_nova_janela(f))


def iniciar_aplicacao():
    root = tk.Tk()
    root.bind('<Escape>', lambda e: root.destroy())
    menu_principal(root)
    root.mainloop()
