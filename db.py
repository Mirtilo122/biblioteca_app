import mysql.connector

def get_connection():
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

def execute_script(script_path):
    print("Iniciando execução")
    with open(script_path, 'r', encoding='utf-8') as f:
        script = f.read()
    print("Script lido")

    conn = get_connection()
    print("Conexão feita com sucesso")
    cursor = conn.cursor()
    try:
        for statement in script.split(';'):
            if statement.strip():
                cursor.execute(statement)
        conn.commit()
        print(f"Script {script_path} executado com sucesso!")
    except mysql.connector.Error as e:
        print(f"Erro ao executar {script_path}: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

def execute_query(query, params=None):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()
        return cursor
    except mysql.connector.Error as e:
        print(f"Erro: {e}")
    finally:
        cursor.close()
        conn.close()
