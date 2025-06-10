import tkinter as tk
from tkinter import messagebox
from crud import (
    listar_usuarios,
    obter_usuario,
    inserir_usuario,
    atualizar_usuario,
    deletar_usuario
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

def usuarios_page(root):
    # Limpa a janela principal
    for w in root.winfo_children():
        w.destroy()

    root.title("Usuários")
    container = tk.Frame(root, bg=COR_BG)
    container.pack(fill="both", expand=True, padx=20, pady=20)

    # Título
    tk.Label(
        container,
        text="Gerenciar Usuários",
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
        text="+ Novo Usuário",
        font=FONTE,
        bg=COR_BOTAO,
        fg="white",
        relief="flat",
        padx=15,
        pady=8,
        command=lambda: mostrar_formulario_usuario(root, container)
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

    def render_usuarios():
        for w in scroll_frame.winfo_children():
            w.destroy()

        for u in listar_usuarios():
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

            titulo = f"Usuário ID: {u['ID']}"
            tk.Label(
                info_frame,
                text=titulo,
                font=("Segoe UI", 14, "bold"),
                fg=COR_HEADER,
                bg=COR_CARD
            ).pack(anchor="w")

            meta = f"Nome: {u['Nome']} | Email: {u['Email']}"
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
                command=lambda reg=u: ver_usuario(reg)
            ).pack(side="left", padx=5)

            tk.Button(
                botoes,
                text="Editar",
                bg=COR_EDIT,
                fg="white",
                font=FONTE,
                relief="flat",
                command=lambda reg=u: mostrar_formulario_usuario(root, container, reg)
            ).pack(side="left", padx=5)

            tk.Button(
                botoes,
                text="Excluir",
                bg="#b00020",
                fg="white",
                font=FONTE,
                relief="flat",
                command=lambda reg=u: confirmar_exclusao(reg)
            ).pack(side="left", padx=5)

    def confirmar_exclusao(u):
        if messagebox.askyesno("Confirmação", "Deseja excluir este usuário?"):
            deletar_usuario(u["ID"])
            messagebox.showinfo("Removido", "Usuário excluído.")
            render_usuarios()

    render_usuarios()

def ver_usuario(u):
    info = "\n".join([f"{k}: {v}" for k, v in u.items()])
    messagebox.showinfo("Detalhes do Usuário", info)

def mostrar_formulario_usuario(root, container, usuario=None):
    # Limpa a janela
    for w in root.winfo_children():
        w.destroy()

    form = tk.Frame(root, bg=COR_BG)
    form.pack(fill="both", expand=True, padx=20, pady=20)

    # Título do formulário
    tk.Label(
        form,
        text="Editar Usuário" if usuario else "Novo Usuário",
        font=("Segoe UI", 16, "bold"),
        bg=COR_BG,
        fg=COR_HEADER
    ).pack(pady=10)

    campos = ['Nome', 'Email', 'CPF', 'Telefone']
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
        if usuario:
            e.insert(0, usuario[c])
        e.pack(fill="x")
        entradas[c] = e

    def salvar():
        try:
            dados = [entradas[c].get().strip() for c in campos]
            if not all(dados[:2]):  # Verifica se Nome e Email não estão vazios
                messagebox.showerror("Erro", "Os campos Nome e Email são obrigatórios.")
                return

            if usuario:
                atualizar_usuario(usuario["ID"], *dados)
                messagebox.showinfo("Sucesso", "Usuário atualizado com sucesso.")
            else:
                inserir_usuario(*dados)
                messagebox.showinfo("Sucesso", "Usuário adicionado com sucesso.")

            usuarios_page(root)

        except Exception as e:
            messagebox.showerror("Erro ao salvar", str(e))

    def voltar():
        usuarios_page(root)

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

    if usuario:
        def excluir():
            if messagebox.askyesno("Confirmação", "Deseja excluir este usuário?"):
                deletar_usuario(usuario["ID"])
                messagebox.showinfo("Removido", "Usuário excluído.")
                usuarios_page(root)

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