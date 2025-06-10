import mysql.connector

def get_connection():
    """
    Estabelece conexão com o banco de dados MySQL.
    """
    print("Iniciando conexão com o banco de dados")
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='123123',
            database='bibliotecadb'
        )
        print("Conexão realizada com sucesso.")
        return conn
    except mysql.connector.Error as e:
        print(f"Erro ao conectar com o banco de dados: {e}")
        raise

def execute_query(query, params=None):
    """
    Executa uma consulta SQL com parâmetros opcionais.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params or ())
        conn.commit()
        return cursor
    except mysql.connector.Error as e:
        print(f"Erro ao executar a consulta: {e}")
        raise
    finally:
        cursor.close()
        conn.close()