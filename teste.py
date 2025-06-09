import pymysql

try:
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='bibliotecadb'
    )
    print("Conexão com MySQL via PyMySQL estabelecida!")

    with conn.cursor() as cursor:
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print("Versão do MySQL:", version[0])

except pymysql.MySQLError as erro:
    print("Erro ao conectar:", erro)

finally:
    if conn:
        conn.close()
        print("Conexão encerrada.")
