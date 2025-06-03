from db import execute_query, get_connection

def inserir_livro():
    titulo = input("Título: ")
    autor = input("Autor: ")
    editora = input("Editora: ")
    genero = input("Gênero: ")
    ano = int(input("Ano: "))
    isbn = input("ISBN: ")
    quantidade = int(input("Quantidade Disponível: "))

    query = '''
    INSERT INTO Livros (Titulo, Autor, Editora, Genero, Ano, ISBN, QuantidadeDisponivel)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    '''
    execute_query(query, (titulo, autor, editora, genero, ano, isbn, quantidade))
    print("Livro inserido com sucesso.")

def fetch_all(query, params=None):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        resultados = cursor.fetchall()
        return resultados
    except Exception as e:
        print(f"Erro ao buscar dados: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def listar_livros():
    livros = fetch_all("SELECT * FROM Livros")
    print("\nLivros cadastrados:")
    for livro in livros:
        print(livro)

def atualizar_livro():
    id_livro = int(input("ID do Livro: "))
    novo_titulo = input("Novo Título: ")

    query = "UPDATE Livros SET Titulo = %s WHERE ID = %s"
    execute_query(query, (novo_titulo, id_livro))
    print("Livro atualizado.")

def deletar_livro():
    id_livro = int(input("ID do Livro a deletar: "))
    query = "DELETE FROM Livros WHERE ID = %s"
    execute_query(query, (id_livro,))
    print("Livro deletado.")
