import tkinter as tk
from tkinter import messagebox, filedialog
from crud import (
    listar_livros, obter_livro, inserir_livro, atualizar_livro, deletar_livro
)
from PIL import Image, ImageTk

def livros_page(root):
    janela = tk.Toplevel(root)
    janela.title("Lista de Livros")
    frame = tk.Frame(janela)
    frame.pack(padx=10, pady=10)

    campos = ['Titulo', 'Autor', 'ImagemURL', 'Editora', 'Genero', 'Ano', 'ISBN', 'QuantidadeDisponivel']

    def carregar():
        for w in frame.winfo_children():
            w.destroy()
        for reg in listar_livros():
            info = " - ".join(f"{k}: {reg[k]}" for k in reg)
            tk.Label(frame, text=info).pack(anchor='w')
            tk.Button(frame, text="Ver", command=lambda r=reg: ver(r['ID'])).pack(anchor='w')
            tk.Button(frame, text="Editar", command=lambda r=reg: editar(r['ID'])).pack(anchor='w')
            tk.Label(frame, text="—"*50).pack()

    def adicionar():
        janela_add = tk.Toplevel(janela)
        janela_add.title("Adicionar Livro")
        entradas = {}

        for campo in campos:
            tk.Label(janela_add, text=campo).pack()
            if campo == 'ImagemURL':
                caminho = tk.StringVar()
                lbl = tk.Label(janela_add, text="Nenhuma imagem selecionada")
                lbl.pack()
                def sel_img(cvar=caminho, l=lbl):
                    f = filedialog.askopenfilename(filetypes=[("Imagens","*.png *.jpg *.jpeg *.gif")])
                    if f: cvar.set(f); l.config(text=f)
                tk.Button(janela_add, text="Selecionar Imagem", command=sel_img).pack()
                entradas[campo] = caminho
            else:
                e = tk.Entry(janela_add); e.pack(); entradas[campo] = e

        def salvar():
            try:
                dados = [entradas[c].get() for c in campos]
                inserir_livro(*dados)
                messagebox.showinfo("Sucesso","Livro adicionado!")
                janela_add.destroy(); carregar()
            except Exception as e:
                messagebox.showerror("Erro", str(e))
        tk.Button(janela_add, text="Salvar", command=salvar).pack()

    def ver(id_livro):
        reg = obter_livro(id_livro)
        if not reg:
            messagebox.showerror("Erro","Livro não encontrado!"); return
        janela_v = tk.Toplevel(janela); janela_v.title("Ver Livro")
        for k,v in reg.items():
            tk.Label(janela_v, text=f"{k}: {v}").pack()
        if reg.get('ImagemURL'):
            try:
                img = Image.open(reg['ImagemURL']).resize((200,300))
                img_tk = ImageTk.PhotoImage(img)
                lbl = tk.Label(janela_v, image=img_tk)
                lbl.image = img_tk; lbl.pack(pady=10)
            except Exception as e:
                tk.Label(janela_v, text=f"Erro imagem: {e}").pack()

    def editar(id_livro):
        reg = obter_livro(id_livro)
        if not reg:
            messagebox.showerror("Erro","Livro não encontrado!"); return
        janela_e = tk.Toplevel(janela); janela_e.title("Editar Livro")
        entradas = {}
        for campo in campos:
            tk.Label(janela_e, text=campo).pack()
            if campo == 'ImagemURL':
                caminho = tk.StringVar(value=reg[campo])
                if reg[campo]:
                    try:
                        img = Image.open(reg[campo]).resize((200,300))
                        tk_img = ImageTk.PhotoImage(img)
                        lbl_img = tk.Label(janela_e, image=tk_img)
                        lbl_img.image = tk_img; lbl_img.pack(pady=5)
                    except: pass
                lbl = tk.Label(janela_e, text=reg[campo] or "Nenhuma imagem selecionada")
                lbl.pack()
                def alt_img(cvar=caminho, l=lbl):
                    f = filedialog.askopenfilename(filetypes=[("Imagens","*.png *.jpg *.jpeg *.gif")])
                    if f: cvar.set(f); l.config(text=f)
                tk.Button(janela_e, text="Alterar Imagem", command=alt_img).pack()
                entradas[campo] = caminho
            else:
                e = tk.Entry(janela_e)
                e.insert(0, reg[campo])
                e.pack()
                entradas[campo] = e

        def salvar():
            try:
                dados = [entradas[c].get() for c in campos]
                atualizar_livro(id_livro, *dados)
                messagebox.showinfo("Sucesso","Livro atualizado!")
                janela_e.destroy(); carregar()
            except Exception as e:
                messagebox.showerror("Erro", str(e))

        def excluir():
            if messagebox.askyesno("Confirmar","Excluir este livro?"):
                deletar_livro(id_livro)
                messagebox.showinfo("Sucesso","Livro deletado!")
                janela_e.destroy(); carregar()

        tk.Button(janela_e, text="Salvar", command=salvar).pack(pady=5)
        tk.Button(janela_e, text="Excluir", fg="red", command=excluir).pack(pady=5)

    tk.Button(janela, text="Adicionar Livro", command=adicionar).pack(pady=10)
    carregar()
