import tkinter as tk
from tkinter import messagebox
from crud import (
    listar_funcionarios,
    obter_funcionario,
    inserir_funcionario,
    atualizar_funcionario,
    deletar_funcionario
)

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

def funcionarios_page(root):
    # Limpa a janela principal
    for w in root.winfo_children():
        w.destroy()

    root.title("Funcionários")
    container = tk.Frame(root, bg=COR_BG)
    container.pack(fill="both", expand=True, padx=20, pady=20)

    # Título
    tk.Label(
        container,
        text="Gerenciar Funcionários",
        font=("Segoe UI", 20, "bold"),
        bg=COR_BG,
        fg=COR_HEADER
    ).pack(pady=(0, 20))

    # Botões topo
    topo = tk.Frame(container, bg=COR_BG)
    topo.pack(fill="x", pady=(0, 20))

    def voltar_inicio():
        from pages.menu_page import menu_principal
        menu_principal(root)

    tk.Button(
        topo,
        text="← Voltar ao Início",
        font=FONTE,
        bg=COR_BOTAO,
        fg="white",
        relief="flat",
        padx=10,
        pady=5,
        command=voltar_inicio
    ).pack(side="left")

    tk.Button(
        topo,
        text="+ Novo Funcionário",
        font=FONTE,
        bg=COR_BOTAO,
        fg="white",
        relief="flat",
        padx=15,
        pady=8,
        command=lambda: mostrar_formulario_funcionario(root, container)
    ).pack(side="right")

    # Área com scroll
    canvas = tk.Canvas(container, bg=COR_BG, highlightthickness=0)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg=COR_BG)

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def render_funcionarios():
        for w in scroll_frame.winfo_children():
            w.destroy()

        for f in listar_funcionarios():
            card = tk.Frame(
                scroll_frame,
                bg=COR_CARD,
                bd=1,
                relief="groove",
                padx=20,
                pady=15
            )
            card.pack(pady=10, fill="x")

            info_frame = tk.Frame(card, bg=COR_CARD)
            info_frame.pack(side="left", fill="x", expand=True)

            titulo = f"Funcionário ID: {f['ID']}"
            tk.Label(
                info_frame,
                text=titulo,
                font=("Segoe UI", 14, "bold"),
                fg=COR_HEADER,
                bg=COR_CARD
            ).pack(anchor="w")

            meta = f"Nome: {f['Nome']} | Cargo: {f['Cargo']}"
            tk.Label(
                info_frame,
                text=meta,
                font=FONTE,
                fg=COR_META,
                bg=COR_CARD
            ).pack(anchor="w", pady=(5, 0))

            botoes = tk.Frame(card, bg=COR_CARD)
            botoes.pack(side="right")

            tk.Button(
                botoes,
                text="Ver",
                bg=COR_VIEW,
                fg="white",
                font=FONTE,
                relief="flat",
                command=lambda reg=f: ver_funcionario(reg)
            ).pack(side="left", padx=5)

            tk.Button(
                botoes,
                text="Editar",
                bg=COR_EDIT,
                fg="white",
                font=FONTE,
                relief="flat",
                command=lambda reg=f: mostrar_formulario_funcionario(root, container, reg)
            ).pack(side="left", padx=5)

            tk.Button(
                botoes,
                text="Excluir",
                bg="#b00020",
                fg="white",
                font=FONTE,
                relief="flat",
                command=lambda reg=f: confirmar_exclusao(reg)
            ).pack(side="left", padx=5)

    def confirmar_exclusao(f):
        if messagebox.askyesno("Confirmação", "Deseja excluir este funcionário?"):
            deletar_funcionario(f["ID"])
            messagebox.showinfo("Removido", "Funcionário excluído.")
            render_funcionarios()

    render_funcionarios()

def ver_funcionario(f):
    info = "\n".join([f"{k}: {v}" for k, v in f.items()])
    messagebox.showinfo("Detalhes do Funcionário", info)

def mostrar_formulario_funcionario(root, container, funcionario=None):
    # Limpa a janela
    for w in root.winfo_children():
        w.destroy()

    form = tk.Frame(root, bg=COR_BG)
    form.pack(fill="both", expand=True, padx=20, pady=20)

    # Título do formulário
    tk.Label(
        form,
        text="Editar Funcionário" if funcionario else "Novo Funcionário",
        font=("Segoe UI", 16, "bold"),
        bg=COR_BG,
        fg=COR_HEADER
    ).pack(pady=10)

    campos = ['Nome', 'Cargo', 'Login', 'Senha']
    entradas = {}

    # Cria campos de entrada
    for c in campos:
        tk.Label(
            form,
            text=c,
            bg=COR_BG,
            fg=COR_FG,
            font=FONTE
        ).pack(anchor="w", pady=(10, 0))
        e = tk.Entry(form, font=FONTE)
        if funcionario:
            e.insert(0, funcionario[c])
        if c == 'Senha':
            e.config(show="*")  # Oculta a senha
        e.pack(fill="x")
        entradas[c] = e

    def salvar():
        try:
            dados = [entradas[c].get().strip() for c in campos]
            if not all(dados[:3]):  # Verifica se Nome, Cargo e Login não estão vazios
                messagebox.showerror("Erro", "Os campos Nome, Cargo e Login são obrigatórios.")
                return

            if funcionario:
                atualizar_funcionario(funcionario["ID"], *dados)
                messagebox.showinfo("Sucesso", "Funcionário atualizado com sucesso.")
            else:
                inserir_funcionario(*dados)
                messagebox.showinfo("Sucesso", "Funcionário adicionado com sucesso.")

            funcionarios_page(root)

        except Exception as e:
            messagebox.showerror("Erro ao salvar", str(e))

    def voltar():
        funcionarios_page(root)

    # Botões
    tk.Button(
        form,
        text="Salvar",
        bg=COR_VIEW,
        fg="white",
        font=FONTE,
        relief="flat",
        command=salvar
    ).pack(pady=10)

    if funcionario:
        def excluir():
            if messagebox.askyesno("Confirmação", "Deseja excluir este funcionário?"):
                deletar_funcionario(funcionario["ID"])
                messagebox.showinfo("Removido", "Funcionário excluído.")
                funcionarios_page(root)

        tk.Button(
            form,
            text="Excluir",
            bg="#b00020",
            fg="white",
            font=FONTE,
            relief="flat",
            command=excluir
        ).pack(pady=5)

    tk.Button(
        form,
        text="← Voltar",
        bg=COR_BOTAO,
        fg="white",
        relief="flat",
        command=voltar
    ).pack(pady=5)