import tkinter as tk
from pages.livros_page import livros_page
from pages.usuarios_page import usuarios_page
from pages.funcionarios_page import funcionarios_page
from pages.emprestimos_page import emprestimos_page

def menu_principal():
    root = tk.Tk()
    root.title("Biblioteca")
    tk.Button(root, text="Livros", width=20, height=2,
              command=lambda: livros_page(root)).pack(pady=10)
    tk.Button(root, text="Usuários", width=20, height=2,
              command=lambda: usuarios_page(root)).pack(pady=10)
    tk.Button(root, text="Funcionários", width=20, height=2,
              command=lambda: funcionarios_page(root)).pack(pady=10)
    tk.Button(root, text="Empréstimos", width=20, height=2,
              command=lambda: emprestimos_page(root)).pack(pady=10)
    root.mainloop()
 