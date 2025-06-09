import tkinter as tk
from tkinter import messagebox
from crud import (
    listar_emprestimos, obter_emprestimo, inserir_emprestimo, atualizar_emprestimo,
    deletar_emprestimo, listar_livros_disponiveis, listar_historico_emprestimos,
    listar_emprestimos_vencidos
)
from datetime import datetime

# Estilos
FONTE = ("Segoe UI", 10)
COR_BG = "#f5f7fa"
COR_FG = "#333333"
COR_HEADER = "#2c3e50"
COR_BOTAO = "#3498db"
COR_VIEW = "#1abc9c"
COR_EDIT = "#f39c12"
COR_CARD = "#ffffff"
COR_META = "#7f8c8d"

def emprestimos_page(root):
    root.title("Empréstimos")
    for w in root.winfo_children():
        w.destroy()

    container = tk.Frame(root, bg=COR_BG)
    container.pack(fill="both", expand=True, padx=20, pady=20)

    tk.Label(container, text="Gerenciar Empréstimos", font=("Segoe UI", 20, "bold"),
             bg=COR_BG, fg=COR_HEADER).pack(pady=(0, 20))

    # Botões topo
    topo = tk.Frame(container, bg=COR_BG)
    topo.pack(fill="x", pady=(0, 20))

    def voltar_inicio():
        from pages.menu_page import menu_principal
        menu_principal(root)

    tk.Button(topo, text="← Voltar ao Início", font=FONTE,
              bg=COR_BOTAO, fg="white", relief="flat", padx=10, pady=5,
              command=voltar_inicio).pack(side="left")

    tk.Button(topo, text="+ Novo Empréstimo", font=FONTE,
              bg=COR_BOTAO, fg="white", relief="flat", padx=15, pady=8,
              command=lambda: mostrar_formulario_emprestimo(root, container)).pack(side="right")

    # Scroll
    canvas = tk.Canvas(container, bg=COR_BG, highlightthickness=0)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg=COR_BG)

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def render_emprestimos():
        for w in scroll_frame.winfo_children():
            w.destroy()

        for e in listar_emprestimos():
            card = tk.Frame(scroll_frame, bg=COR_CARD, bd=1, relief="groove", padx=20, pady=15)
            card.pack(pady=10, fill="x")

            info_frame = tk.Frame(card, bg=COR_CARD)
            info_frame.pack(side="left", fill="x", expand=True)

            titulo = f"Empréstimo ID: {e['ID']}"
            tk.Label(info_frame, text=titulo, font=("Segoe UI", 14, "bold"),
                     fg=COR_HEADER, bg=COR_CARD).pack(anchor="w")

            meta = f"Livro: {e['IDLivro']} | Usuário: {e['IDUsuario']} | Funcionário: {e['IDFuncionario']}"
            status = f"Data Empréstimo: {e['DataEmprestimo']} | Devolução: {e['DataDevolucao']} | Status: {e['Status']}"
            tk.Label(info_frame, text=meta, font=FONTE, fg=COR_META, bg=COR_CARD).pack(anchor="w", pady=(5, 0))
            tk.Label(info_frame, text=status, font=FONTE, fg=COR_META, bg=COR_CARD).pack(anchor="w", pady=(2, 0))

            botoes = tk.Frame(card, bg=COR_CARD)
            botoes.pack(side="right")

            tk.Button(botoes, text="Ver", bg=COR_VIEW, fg="white", font=FONTE, relief="flat",
                      command=lambda reg=e: ver_emprestimo(reg)).pack(side="left", padx=5)
            tk.Button(botoes, text="Editar", bg=COR_EDIT, fg="white", font=FONTE, relief="flat",
                      command=lambda reg=e: mostrar_formulario_emprestimo(root, container, reg)).pack(side="left", padx=5)

    render_emprestimos()

def ver_emprestimo(e):
    info = "\n".join([f"{k}: {v}" for k, v in e.items()])
    messagebox.showinfo("Detalhes do Empréstimo", info)
def mostrar_formulario_emprestimo(root, container, emprestimo=None):
    for w in root.winfo_children():
        w.destroy()

    form = tk.Frame(root, bg=COR_BG)
    form.pack(fill="both", expand=True, padx=20, pady=20)

    tk.Label(form, text="Editar Empréstimo" if emprestimo else "Novo Empréstimo",
             font=("Segoe UI", 16, "bold"), bg=COR_BG, fg=COR_HEADER).pack(pady=10)

    campos = ['IDLivro', 'IDUsuario', 'IDFuncionario', 'DataEmprestimo', 'DataDevolucao', 'Status']
    entradas = {}

    for c in campos:
        tk.Label(form, text=c, bg=COR_BG, fg=COR_FG, font=FONTE).pack(anchor="w", pady=(10, 0))
        e = tk.Entry(form, font=FONTE)
        if emprestimo:
            value = emprestimo[c]
            if c in ['DataEmprestimo', 'DataDevolucao'] and value:
                try:
                    date_obj = datetime.strptime(value, "%d/%m/%Y")
                    value = date_obj.strftime("%Y-%m-%d")
                except ValueError:
                    pass  # Keep original value if format is invalid
            e.insert(0, value)
        e.pack(fill="x")
        entradas[c] = e

    def salvar():
        try:
            dados = [entradas[c].get().strip() for c in campos]

            for campo in ['DataEmprestimo', 'DataDevolucao']:
                valor = entradas[campo].get().strip()
                if valor:
                    try:
                        datetime.strptime(valor, "%Y-%m-%d")
                    except ValueError:
                        messagebox.showerror("Erro", f"O campo '{campo}' deve estar no formato YYYY-MM-DD.")
                        return

            if emprestimo:
                atualizar_emprestimo(emprestimo["ID"], *dados)
            else:
                inserir_emprestimo(*dados)

            messagebox.showinfo("Sucesso", "Dados salvos com sucesso.")
            emprestimos_page(root)

        except Exception as e:
            messagebox.showerror("Erro ao salvar", str(e))

    def voltar():
        emprestimos_page(root)

    tk.Button(form, text="Salvar", bg=COR_VIEW, fg="white", font=FONTE,
              relief="flat", command=salvar).pack(pady=10)

    if emprestimo:
        def excluir():
            if messagebox.askyesno("Confirmação", "Deseja excluir este empréstimo?"):
                deletar_emprestimo(emprestimo["ID"])
                messagebox.showinfo("Removido", "Empréstimo excluído.")
                emprestimos_page(root)

        tk.Button(form, text="Excluir", bg="#b00020", fg="white", font=FONTE,
                  relief="flat", command=excluir).pack()

    tk.Button(form, text="← Voltar", command=voltar, bg=COR_BOTAO,
              fg="white", relief="flat").pack(pady=5)
