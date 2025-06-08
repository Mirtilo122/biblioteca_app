import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
from crud import listar_livros, obter_livro, inserir_livro, atualizar_livro, deletar_livro

FONTE = ("Segoe UI", 10)
COR_BG = "#f5f7fa"
COR_FG = "#333333"
COR_HEADER = "#2c3e50"
COR_BOTAO = "#3498db"
COR_BOTAO_HOVER = "#2980b9"
COR_CARD = "#ffffff"
COR_META = "#7f8c8d"
COR_VIEW = "#1abc9c"
COR_EDIT = "#f39c12"
COR_VIEW_HOVER = "#16a085"
COR_EDIT_HOVER = "#d68910"

def livros_page(root):
    root.title("Biblioteca Virtual")
    for w in root.winfo_children():
        w.destroy()

    container = tk.Frame(root, bg=COR_BG)
    container.pack(fill="both", expand=True, padx=20, pady=20)

    # Título
    tk.Label(container, text="Biblioteca Virtual", font=("Segoe UI", 20, "bold"),
             bg=COR_BG, fg=COR_HEADER).pack(pady=(0, 20))

    # Botão Adicionar
    tk.Button(container, text="+ Adicionar Novo Livro", font=FONTE,
              bg=COR_BOTAO, fg="white", padx=15, pady=8, bd=0,
              relief="flat", command=lambda: mostrar_formulario_livro(root, container)
              ).pack(pady=(0, 20))

    # Área de rolagem
    canvas = tk.Canvas(container, bg=COR_BG, highlightthickness=0)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg=COR_BG)

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

def livros_page(root):
    root.title("Biblioteca Virtual")
    for w in root.winfo_children():
        w.destroy()

    container = tk.Frame(root, bg=COR_BG)
    container.pack(fill="both", expand=True, padx=20, pady=20)

    # Título
    tk.Label(container, text="Biblioteca Virtual", font=("Segoe UI", 20, "bold"),
             bg=COR_BG, fg=COR_HEADER).pack(pady=(0, 20))

    # Botões superiores
    botoes_topo = tk.Frame(container, bg=COR_BG)
    botoes_topo.pack(pady=(0, 20), fill="x")

    tk.Button(botoes_topo, text="← Voltar ao Início", font=FONTE,
          bg=COR_BOTAO, fg="white", padx=10, pady=5, bd=0,
          relief="flat", command=lambda: menu_principal(root)).pack(side="left")

    tk.Button(botoes_topo, text="+ Adicionar Novo Livro", font=FONTE,
              bg=COR_BOTAO, fg="white", padx=15, pady=8, bd=0,
              relief="flat", command=lambda: mostrar_formulario_livro(root, container)
              ).pack(side="right")

    # Área de rolagem
    canvas = tk.Canvas(container, bg=COR_BG, highlightthickness=0)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg=COR_BG)

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def render_livros():
        for w in scroll_frame.winfo_children():
            w.destroy()

        for livro in listar_livros():
            card = tk.Frame(scroll_frame, bg=COR_CARD, bd=1, relief="groove", padx=20, pady=15)
            card.pack(pady=15, fill="x")

            # Informações
            info_frame = tk.Frame(card, bg=COR_CARD)
            info_frame.pack(side="left", fill="x", expand=True)

            titulo = tk.Label(info_frame, text=livro["Titulo"], font=("Segoe UI", 14, "bold"),
                              fg=COR_HEADER, bg=COR_CARD)
            titulo.pack(anchor="w")

            meta_text = f"Gênero: {livro['Genero']} | Autor: {livro['Autor']} | Disponível: {livro['QuantidadeDisponivel']}"
            meta = tk.Label(info_frame, text=meta_text, font=("Segoe UI", 11), fg=COR_META, bg=COR_CARD)
            meta.pack(anchor="w", pady=(5, 0))

            # Botões
            botoes_frame = tk.Frame(card, bg=COR_CARD)
            botoes_frame.pack(side="right")

            tk.Button(botoes_frame, text="Ver", bg=COR_VIEW, fg="white", font=FONTE, relief="flat",
                      command=lambda l=livro: ver_livro(l)).pack(side="left", padx=5)
            tk.Button(botoes_frame, text="Editar", bg=COR_EDIT, fg="white", font=FONTE, relief="flat",
                      command=lambda l=livro: mostrar_formulario_livro(root, container, livro)).pack(side="left", padx=5)

    render_livros()


def ver_livro(livro):
    info = "\n".join([f"{k}: {v}" for k, v in livro.items()])
    messagebox.showinfo("Informações do Livro", info)

def mostrar_formulario_livro(root, container, livro=None):
    for w in root.winfo_children():
        w.destroy()

    form_frame = tk.Frame(root, bg=COR_BG)
    form_frame.pack(fill="both", expand=True, padx=20, pady=20)

    tk.Label(form_frame, text=("Editar Livro" if livro else "Adicionar Novo Livro"),
             font=("Segoe UI", 16, "bold"), bg=COR_BG, fg=COR_HEADER).pack(pady=10)

    campos = ['Titulo', 'Autor', 'ImagemURL', 'Editora', 'Genero', 'Ano', 'ISBN', 'QuantidadeDisponivel']
    entradas = {}

    for campo in campos:
        tk.Label(form_frame, text=campo, bg=COR_BG, fg=COR_FG, font=FONTE).pack(anchor="w", pady=(10, 0))
        if campo == "ImagemURL":
            var = tk.StringVar(value=livro[campo] if livro else "")
            lbl_img = tk.Label(form_frame, text=var.get() or "Nenhuma imagem selecionada", fg=COR_META, bg=COR_BG)
            lbl_img.pack(anchor="w")

            def selecionar():
                path = filedialog.askopenfilename(filetypes=[("Imagens", "*.png *.jpg *.jpeg *.gif")])
                if path:
                    var.set(path)
                    lbl_img.config(text=path)

            tk.Button(form_frame, text="Selecionar Imagem", command=selecionar, bg=COR_BOTAO, fg="white", relief="flat").pack(anchor="w")
            entradas[campo] = var
        else:
            entry = tk.Entry(form_frame, font=FONTE)
            if livro: entry.insert(0, livro[campo])
            entry.pack(fill="x")
            entradas[campo] = entry

    def voltar():
        livros_page(root)

    def salvar():
        try:
            dados = [entradas[c].get() if not isinstance(entradas[c], tk.StringVar) else entradas[c].get() for c in campos]
            if livro:
                atualizar_livro(livro["ID"], *dados)
            else:
                inserir_livro(*dados)
            messagebox.showinfo("Sucesso", "Livro salvo com sucesso.")
            livros_page(root)
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    tk.Button(form_frame, text="Salvar", bg=COR_VIEW, fg="white", font=FONTE, relief="flat", command=salvar).pack(pady=10)
    if livro:
        def excluir():
            if messagebox.askyesno("Confirmação", "Deseja excluir este livro?"):
                deletar_livro(livro["ID"])
                messagebox.showinfo("Removido", "Livro excluído com sucesso.")
                livros_page(root)
        tk.Button(form_frame, text="Excluir", bg="#b00020", fg="white", font=FONTE, relief="flat", command=excluir).pack()

    tk.Button(form_frame, text="← Voltar", command=voltar, bg=COR_BOTAO, fg="white", relief="flat").pack(pady=5)


