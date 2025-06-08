import tkinter as tk
from tkinter import messagebox
from crud import (
    listar_emprestimos, obter_emprestimo, inserir_emprestimo, atualizar_emprestimo,
    deletar_emprestimo, listar_livros_disponiveis, listar_historico_emprestimos,
    listar_emprestimos_vencidos
)

def emprestimos_page(root):
    janela = tk.Toplevel(root)
    janela.title("Lista de Empréstimos")
    frame = tk.Frame(janela); frame.pack(padx=10, pady=10)
    campos = ['IDLivro', 'IDUsuario', 'IDFuncionario', 'DataEmprestimo', 'DataDevolucao', 'Status']

    def carregar():
        for w in frame.winfo_children(): w.destroy()
        for reg in listar_emprestimos():
            info = " - ".join(f"{k}: {reg[k]}" for k in reg)
            tk.Label(frame, text=info).pack(anchor='w')
            tk.Button(frame, text="Ver", command=lambda r=reg: ver(r['ID'])).pack(anchor='w')
            tk.Button(frame, text="Editar", command=lambda r=reg: editar(r['ID'])).pack(anchor='w')
            tk.Label(frame, text="—"*50).pack()

    def adicionar():
        janela_add = tk.Toplevel(janela); janela_add.title("Adicionar Empréstimo")
        entradas = {}
        for c in campos:
            tk.Label(janela_add, text=c).pack()
            e = tk.Entry(janela_add); e.pack(); entradas[c] = e

        def salvar():
            try:
                dados = [entradas[c].get() for c in campos]
                inserir_emprestimo(*dados)
                messagebox.showinfo("Sucesso","Empréstimo adicionado!")
                janela_add.destroy(); carregar()
            except Exception as e:
                messagebox.showerror("Erro", str(e))

        tk.Button(janela_add, text="Salvar", command=salvar).pack()

    def ver(id_e):
        reg = obter_emprestimo(id_e)
        if not reg:
            messagebox.showerror("Erro","Empréstimo não encontrado!"); return
        janela_v = tk.Toplevel(janela); janela_v.title("Ver Empréstimo")
        for k,v in reg.items():
            tk.Label(janela_v, text=f"{k}: {v}").pack()

    def editar(id_e):
        reg = obter_emprestimo(id_e)
        if not reg:
            messagebox.showerror("Erro","Empréstimo não encontrado!"); return
        janela_e = tk.Toplevel(janela); janela_e.title("Editar Empréstimo")
        entradas = {}
        for c in campos:
            tk.Label(janela_e, text=c).pack()
            e = tk.Entry(janela_e); e.insert(0, reg[c]); e.pack(); entradas[c] = e

        def salvar():
            try:
                dados = [entradas[c].get() for c in campos]
                atualizar_emprestimo(id_e, *dados)
                messagebox.showinfo("Sucesso","Empréstimo atualizado!")
                janela_e.destroy(); carregar()
            except Exception as e:
                messagebox.showerror("Erro", str(e))

        def excluir():
            if messagebox.askyesno("Confirmar", "Excluir este empréstimo?"):
                deletar_emprestimo(id_e)
                messagebox.showinfo("Sucesso","Empréstimo excluído!")
                janela_e.destroy(); carregar()

        tk.Button(janela_e, text="Salvar", command=salvar).pack(pady=5)
        tk.Button(janela_e, text="Excluir", fg="red", command=excluir).pack(pady=5)

    # Botões de visualização extra
    tk.Button(janela, text="Livros Disponíveis", width=20,
              command=lambda: view(listar_livros_disponiveis, "Livros Disponíveis")).pack(pady=5)
    tk.Button(janela, text="Histórico de Empréstimos", width=20,
              command=lambda: view(listar_historico_emprestimos, "Histórico de Empréstimos")).pack(pady=5)
    tk.Button(janela, text="Empréstimos Vencidos", width=20,
              command=lambda: view(listar_emprestimos_vencidos, "Empréstimos Vencidos")).pack(pady=5)

    def view(func, title):
        v = tk.Toplevel(janela); v.title(title)
        for reg in func():
            info = " - ".join(f"{k}: {reg[k]}" for k in reg)
            tk.Label(v, text=info).pack(anchor='w')

    tk.Button(janela, text="Adicionar Empréstimo", command=adicionar).pack(pady=10)
    carregar()
