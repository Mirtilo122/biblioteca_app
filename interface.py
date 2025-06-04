import tkinter as tk 
from tkinter import messagebox, simpledialog, filedialog
from crud import (
    listar_livros, inserir_livro, obter_livro, atualizar_livro, deletar_livro,
    listar_usuarios, inserir_usuario, obter_usuario, atualizar_usuario, deletar_usuario,
    listar_funcionarios, inserir_funcionario, obter_funcionario, atualizar_funcionario, deletar_funcionario,
    listar_emprestimos, inserir_emprestimo, obter_emprestimo, atualizar_emprestimo, deletar_emprestimo,
    listar_livros_disponiveis, listar_historico_emprestimos, listar_emprestimos_vencidos,
    registrar_emprestimo, registrar_devolucao
)
from PIL import Image, ImageTk

def menu_principal():
    root = tk.Tk()
    root.title("Biblioteca")

    def abrir_listagem(titulo, listar_func, obter_func, inserir_func, atualizar_func, deletar_func, campos):
        janela = tk.Toplevel(root)
        janela.title(f"Lista de {titulo}")

        def carregar():
            for widget in frame.winfo_children():
                widget.destroy()
            registros = listar_func()
            for registro in registros:
                info = " - ".join(f"{chave}: {registro[chave]}" for chave in registro)
                tk.Label(frame, text=info).pack(anchor='w')

                btn_ver = tk.Button(frame, text="Ver", command=lambda r=registro: ver(r['ID']))
                btn_ver.pack(anchor='w')

                btn_edit = tk.Button(frame, text="Editar", command=lambda r=registro: editar(r['ID']))
                btn_edit.pack(anchor='w')

                tk.Label(frame, text="-" * 50).pack()

        def adicionar():
            janela_add = tk.Toplevel(janela)
            janela_add.title(f"Adicionar {titulo[:-1]}")

            entradas = {}

            for campo in campos:
                tk.Label(janela_add, text=campo).pack()
                
                if titulo == "Livros" and campo == "ImagemURL":
                    # Substitui o campo ImagemURL por um botão de upload
                    caminho_imagem = tk.StringVar()

                    def selecionar_imagem():
                        arquivo = filedialog.askopenfilename(
                            title="Selecione a Imagem",
                            filetypes=[("Imagens", "*.png *.jpg *.jpeg *.gif *.bmp")]
                        )
                        if arquivo:
                            caminho_imagem.set(arquivo)
                            lbl_imagem.config(text=arquivo)

                    btn_upload = tk.Button(janela_add, text="Selecionar Imagem", command=selecionar_imagem)
                    btn_upload.pack()

                    lbl_imagem = tk.Label(janela_add, text="Nenhuma imagem selecionada")
                    lbl_imagem.pack()

                    entradas[campo] = caminho_imagem
                else:
                    entrada = tk.Entry(janela_add)
                    entrada.pack()
                    entradas[campo] = entrada

            def salvar():
                try:
                    dados = []
                    for c in campos:
                        valor = entradas[c].get() if not isinstance(entradas[c], tk.StringVar) else entradas[c].get()
                        dados.append(valor)

                    inserir_func(*dados)
                    messagebox.showinfo("Sucesso", f"{titulo[:-1]} adicionado!")
                    janela_add.destroy()
                    carregar()
                except Exception as e:
                    messagebox.showerror("Erro", str(e))

            tk.Button(janela_add, text="Salvar", command=salvar).pack()

        def ver(id_registro):
            reg = obter_func(id_registro)
            if not reg:
                messagebox.showerror("Erro", f"{titulo[:-1]} não encontrado!")
                return

            janela_ver = tk.Toplevel(janela)
            janela_ver.title(f"Ver {titulo[:-1]}")

            for chave, valor in reg.items():
                tk.Label(janela_ver, text=f"{chave}: {valor}").pack()

            # Se for Livro e tiver ImagemURL, exibe a imagem
            if titulo == "Livros" and 'ImagemURL' in reg and reg['ImagemURL']:
                try:
                    imagem = Image.open(reg['ImagemURL'])
                    imagem = imagem.resize((200, 300))  # Redimensiona conforme necessário
                    imagem_tk = ImageTk.PhotoImage(imagem)
                    label_imagem = tk.Label(janela_ver, image=imagem_tk)
                    label_imagem.image = imagem_tk  # Necessário manter uma referência
                    label_imagem.pack(pady=10)
                except Exception as e:
                    tk.Label(janela_ver, text=f"Erro ao carregar imagem: {e}").pack()

        def editar(id_registro):
            reg = obter_func(id_registro)
            if not reg:
                messagebox.showerror("Erro", f"{titulo[:-1]} não encontrado!")
                return

            janela_edit = tk.Toplevel(janela)
            janela_edit.title(f"Editar {titulo[:-1]}")

            entradas = {}

            for campo in campos:
                tk.Label(janela_edit, text=campo).pack()

                if titulo == "Livros" and campo == "ImagemURL":
                    caminho_imagem = tk.StringVar()
                    caminho_imagem.set(reg[campo])

                    # Exibe imagem atual, se houver
                    if reg[campo]:
                        try:
                            imagem = Image.open(reg[campo])
                            imagem = imagem.resize((200, 300))
                            imagem_tk = ImageTk.PhotoImage(imagem)
                            label_imagem = tk.Label(janela_edit, image=imagem_tk)
                            label_imagem.image = imagem_tk
                            label_imagem.pack(pady=10)
                        except Exception as e:
                            tk.Label(janela_edit, text=f"Erro ao carregar imagem: {e}").pack()

                    lbl_imagem = tk.Label(janela_edit, text=reg[campo] or "Nenhuma imagem selecionada")
                    lbl_imagem.pack()

                    def alterar_imagem():
                        arquivo = filedialog.askopenfilename(
                            title="Alterar Imagem",
                            filetypes=[("Imagens", "*.png *.jpg *.jpeg *.gif *.bmp")]
                        )
                        if arquivo:
                            caminho_imagem.set(arquivo)
                            lbl_imagem.config(text=arquivo)

                    btn_upload = tk.Button(janela_edit, text="Alterar Imagem", command=alterar_imagem)
                    btn_upload.pack()

                    entradas[campo] = caminho_imagem
                else:
                    entrada = tk.Entry(janela_edit)
                    entrada.insert(0, str(reg[campo]))
                    entrada.pack()
                    entradas[campo] = entrada

            def salvar():
                try:
                    dados = []
                    for c in campos:
                        valor = entradas[c].get() if not isinstance(entradas[c], tk.StringVar) else entradas[c].get()
                        dados.append(valor)

                    atualizar_func(id_registro, *dados)
                    messagebox.showinfo("Sucesso", f"{titulo[:-1]} atualizado!")
                    janela_edit.destroy()
                    carregar()
                except Exception as e:
                    messagebox.showerror("Erro", str(e))

            def excluir():
                if messagebox.askyesno("Confirmar", f"Deletar este {titulo[:-1]}?"):
                    deletar_func(id_registro)
                    messagebox.showinfo("Sucesso", f"{titulo[:-1]} deletado!")
                    janela_edit.destroy()
                    carregar()

            tk.Button(janela_edit, text="Salvar Alterações", command=salvar).pack(pady=5)
            tk.Button(janela_edit, text="Deletar", fg="red", command=excluir).pack(pady=5)

        tk.Button(janela, text=f"Adicionar Novo {titulo[:-1]}", command=adicionar).pack(pady=10)

        frame = tk.Frame(janela)
        frame.pack()

        carregar()

        # Botões extras apenas na listagem de empréstimos
        if titulo == "Empréstimos":
            def mostrar_view(view_func, titulo_view):
                janela_view = tk.Toplevel(janela)
                janela_view.title(titulo_view)
                registros = view_func()
                for reg in registros:
                    info = " - ".join(f"{chave}: {reg[chave]}" for chave in reg)
                    tk.Label(janela_view, text=info).pack(anchor='w')

            tk.Button(janela, text="Livros Disponíveis", width=20,
                      command=lambda: mostrar_view(listar_livros_disponiveis, "Livros Disponíveis")).pack(pady=5)

            tk.Button(janela, text="Histórico de Empréstimos", width=20,
                      command=lambda: mostrar_view(listar_historico_emprestimos, "Histórico de Empréstimos")).pack(pady=5)

            tk.Button(janela, text="Empréstimos Vencidos", width=20,
                      command=lambda: mostrar_view(listar_emprestimos_vencidos, "Empréstimos Vencidos")).pack(pady=5)

    # ============ Botões para cada CRUD ============ #

    tk.Button(root, text="Livros", width=20, height=2,
              command=lambda: abrir_listagem(
                  "Livros", listar_livros, obter_livro, inserir_livro, atualizar_livro, deletar_livro,
                  ['Titulo', 'Autor', 'ImagemURL', 'Editora', 'Genero', 'Ano', 'ISBN', 'QuantidadeDisponivel']
              )).pack(pady=10)

    tk.Button(root, text="Usuários", width=20, height=2,
              command=lambda: abrir_listagem(
                  "Usuários", listar_usuarios, obter_usuario, inserir_usuario, atualizar_usuario, deletar_usuario,
                  ['Nome', 'Email', 'CPF', 'Telefone']
              )).pack(pady=10)

    tk.Button(root, text="Funcionários", width=20, height=2,
              command=lambda: abrir_listagem(
                  "Funcionários", listar_funcionarios, obter_funcionario, inserir_funcionario, atualizar_funcionario, deletar_funcionario,
                  ['Nome', 'Cargo', 'Login', 'Senha']
              )).pack(pady=10)

    tk.Button(root, text="Empréstimos", width=20, height=2,
              command=lambda: abrir_listagem(
                  "Empréstimos", listar_emprestimos, obter_emprestimo, inserir_emprestimo, atualizar_emprestimo, deletar_emprestimo,
                  ['IDLivro', 'IDUsuario', 'IDFuncionario', 'DataEmprestimo', 'DataDevolucao', 'Status']
              )).pack(pady=10)

    # Botões para as Procedures
    def executar_registrar_emprestimo():
        try:
            id_livro = int(simpledialog.askstring("Entrada", "ID do Livro:"))
            id_usuario = int(simpledialog.askstring("Entrada", "ID do Usuário:"))
            id_funcionario = int(simpledialog.askstring("Entrada", "ID do Funcionário:"))
            data_devolucao = simpledialog.askstring("Entrada", "Data de Devolução (YYYY-MM-DD):")
            registrar_emprestimo(id_livro, id_usuario, id_funcionario, data_devolucao)
            messagebox.showinfo("Sucesso", "Empréstimo registrado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def executar_registrar_devolucao():
        try:
            id_emprestimo = int(simpledialog.askstring("Entrada", "ID do Empréstimo:"))
            registrar_devolucao(id_emprestimo)
            messagebox.showinfo("Sucesso", "Devolução registrada com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    tk.Button(root, text="Registrar Empréstimo", width=20, height=2,
              command=executar_registrar_emprestimo).pack(pady=10)

    tk.Button(root, text="Registrar Devolução", width=20, height=2,
              command=executar_registrar_devolucao).pack(pady=10)

    tk.Button(root, text="Sair", command=root.quit).pack(pady=10)

    root.mainloop()
