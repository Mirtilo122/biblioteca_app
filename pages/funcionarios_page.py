import tkinter as tk
from tkinter import messagebox
from crud import listar_funcionarios, obter_funcionario, inserir_funcionario, atualizar_funcionario, deletar_funcionario

def funcionarios_page(root):
    janela = tk.Toplevel(root)
    janela.title("Lista de Funcionários")
    frame = tk.Frame(janela); frame.pack(padx=10, pady=10)
    campos = ['Nome', 'Cargo', 'Login', 'Senha']

    def carregar():
        for w in frame.winfo_children(): w.destroy()
        for reg in listar_funcionarios():
            info = " - ".join(f"{k}: {reg[k]}" for k in reg)
            tk.Label(frame, text=info).pack(anchor='w')
            tk.Button(frame, text="Ver", command=lambda r=reg: ver(r['ID'])).pack(anchor='w')
            tk.Button(frame, text="Editar", command=lambda r=reg: editar(r['ID'])).pack(anchor='w')
            tk.Label(frame, text="—"*50).pack()

    def adicionar():
        janela_add = tk.Toplevel(janela); janela_add.title("Adicionar Funcionário")
        entradas = {}
        for c in campos:
            tk.Label(janela_add, text=c).pack()
            e = tk.Entry(janela_add); e.pack(); entradas[c] = e

        def salvar():
            try:
                dados = [entradas[c].get() for c in campos]
                inserir_funcionario(*dados)
                messagebox.showinfo("Sucesso","Funcionário adicionado!")
                janela_add.destroy(); carregar()
            except Exception as e:
                messagebox.showerror("Erro", str(e))

        tk.Button(janela_add, text="Salvar", command=salvar).pack()

    def ver(id_f):
        reg = obter_funcionario(id_f)
        if not reg:
            messagebox.showerror("Erro","Funcionário não encontrado!"); return
        janela_v = tk.Toplevel(janela); janela_v.title("Ver Funcionário")
        for k,v in reg.items():
            tk.Label(janela_v, text=f"{k}: {v}").pack()

    def editar(id_f):
        reg = obter_funcionario(id_f)
        if not reg:
            messagebox.showerror("Erro","Funcionário não encontrado!"); return
        janela_e = tk.Toplevel(janela); janela_e.title("Editar Funcionário")
        entradas = {}
        for c in campos:
            tk.Label(janela_e, text=c).pack()
            e = tk.Entry(janela_e); e.insert(0, reg[c]); e.pack(); entradas[c] = e

        def salvar():
            try:
                dados = [entradas[c].get() for c in campos]
                atualizar_funcionario(id_f, *dados)
                messagebox.showinfo("Sucesso","Funcionário atualizado!")
                janela_e.destroy(); carregar()
            except Exception as e:
                messagebox.showerror("Erro", str(e))

        def excluir():
            if messagebox.askyesno("Confirmar", "Excluir este funcionário?"):
                deletar_funcionario(id_f)
                messagebox.showinfo("Sucesso","Funcionário excluído!")
                janela_e.destroy(); carregar()

        tk.Button(janela_e, text="Salvar", command=salvar).pack(pady=5)
        tk.Button(janela_e, text="Excluir", fg="red", command=excluir).pack(pady=5)

    tk.Button(janela, text="Adicionar Funcionário", command=adicionar).pack(pady=10)
    carregar()
