from crud import inserir_livro, listar_livros, atualizar_livro, deletar_livro

def menu_principal():
    while True:
        print("\nBiblioteca - Menu Principal")
        print("1. Inserir Livro")
        print("2. Listar Livros")
        print("3. Atualizar Livro")
        print("4. Deletar Livro")
        print("5. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            inserir_livro()
        elif opcao == '2':
            listar_livros()
        elif opcao == '3':
            atualizar_livro()
        elif opcao == '4':
            deletar_livro()
        elif opcao == '5':
            print("Saindo...")
            break
        else:
            print("Opção inválida.")
