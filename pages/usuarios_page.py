import tkinter as tk
from tkinter import messagebox
from crud import (
    listar_usuarios, obter_usuario,
    inserir_usuario, atualizar_usuario, deletar_usuario
)

def usuarios_page(root):
    janela = tk.Toplevel(root)
    janela.title("Lista de Usuários")

    frame = tk.Frame(janela)
    frame.pack(padx=10, pady=10)

    def carregar():
        for widget in frame.winfo_children():
            widget.destroy()
        registros = listar_usuarios()
        for registro in registros:
            info = " - ".join(f"{chave}: {registro[chave]}" for chave in registro)
            tk.Label(frame, text=info).pack(anchor='w')

            tk.Button(frame, text="Ver", command=lambda r=registro: ver(r['ID'])).pack(anchor='w')
            tk.Button(frame, text="Editar", command=lambda r=registro: editar(r['ID'])).pack(anchor='w')
            tk.Label(frame, text="-" * 50).pack()

    def adicionar():
        janela_add = tk.Toplevel(janela)
        janela_add.title("Adicionar Usuário")

        entradas = {}
        campos = ['Nome', 'Email', 'CPF', 'Telefone']

        for campo in campos:
            tk.Label(janela_add, text=campo).pack()
            entrada = tk.Entry(janela_add)
            entrada.pack()
            entradas[campo] = entrada

        def salvar():
            try:
                dados = [entradas[c].get() for c in campos]
                inserir_usuario(*dados)
                messagebox.showinfo("Sucesso", "Usuário adicionado!")
                janela_add.destroy()
                carregar()
            except Exception as e:
                messagebox.showerror("Erro", str(e))

        tk.Button(janela_add, text="Salvar", command=salvar).pack()

    def ver(id_usuario):
        reg = obter_usuario(id_usuario)
        if not reg:
            messagebox.showerror("Erro", "Usuário não encontrado!")
            return

        janela_ver = tk.Toplevel(janela)
        janela_ver.title("Ver Usuário")
        for chave, valor in reg.items():
            tk.Label(janela_ver, text=f"{chave}: {valor}").pack()

    def editar(id_usuario):
        reg = obter_usuario(id_usuario)
        if not reg:
            messagebox.showerror("Erro", "Usuário não encontrado!")
            return

        janela_edit = tk.Toplevel(janela)
        janela_edit.title("Editar Usuário")

        entradas = {}
        campos = ['Nome', 'Email', 'CPF', 'Telefone']

        for campo in campos:
            tk.Label(janela_edit, text=campo).pack()
            entrada = tk.Entry(janela_edit)
            entrada.insert(0, reg[campo])
            entrada.pack()
            entradas[campo] = entrada

        def salvar():
            try:
                dados = [entradas[c].get() for c in campos]
                atualizar_usuario(id_usuario, *dados)
                messagebox.showinfo("Sucesso", "Usuário atualizado!")
                janela_edit.destroy()
                carregar()
            except Exception as e:
                messagebox.showerror("Erro", str(e))

        def excluir():
            if messagebox.askyesno("Confirmar", "Deseja excluir este usuário?"):
                try:
                    deletar_usuario(id_usuario)
                    messagebox.showinfo("Sucesso", "Usuário excluído!")
                    janela_edit.destroy()
                    carregar()
                except Exception as e:
                    messagebox.showerror("Erro", str(e))

        tk.Button(janela_edit, text="Salvar", command=salvar).pack()
        tk.Button(janela_edit, text="Excluir", command=excluir).pack()

    tk.Button(janela, text="Adicionar Usuário", command=adicionar).pack(pady=10)
    carregar()