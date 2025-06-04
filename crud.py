from db import execute_query, get_connection

# ------------------------ LIVROS ------------------------

def inserir_livro(titulo, autor, imagem_url, editora, genero, ano, isbn, quantidade):
    query = '''
    INSERT INTO Livros (Titulo, Autor, ImagemURL, Editora, Genero, Ano, ISBN, QuantidadeDisponivel)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    '''
    execute_query(query, (titulo, autor, imagem_url, editora, genero, ano, isbn, quantidade))

def listar_livros():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Livros")
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def obter_livro(id_livro):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Livros WHERE ID = %s", (id_livro,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

def atualizar_livro(id_livro, titulo, autor, imagem_url, editora, genero, ano, isbn, quantidade):
    query = '''
    UPDATE Livros
    SET Titulo = %s, Autor = %s, ImagemURL = %s, Editora = %s,
        Genero = %s, Ano = %s, ISBN = %s, QuantidadeDisponivel = %s
    WHERE ID = %s
    '''
    execute_query(query, (titulo, autor, imagem_url, editora, genero, ano, isbn, quantidade, id_livro))

def deletar_livro(id_livro):
    query = "DELETE FROM Livros WHERE ID = %s"
    execute_query(query, (id_livro,))

# ------------------------ USUÁRIOS ------------------------

def inserir_usuario(nome, email, cpf, telefone):
    query = '''
    INSERT INTO Usuarios (Nome, Email, CPF, Telefone)
    VALUES (%s, %s, %s, %s)
    '''
    execute_query(query, (nome, email, cpf, telefone))

def listar_usuarios():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Usuarios")
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def obter_usuario(id_usuario):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Usuarios WHERE ID = %s", (id_usuario,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

def atualizar_usuario(id_usuario, nome, email, cpf, telefone):
    query = '''
    UPDATE Usuarios
    SET Nome = %s, Email = %s, CPF = %s, Telefone = %s
    WHERE ID = %s
    '''
    execute_query(query, (nome, email, cpf, telefone, id_usuario))

def deletar_usuario(id_usuario):
    query = "DELETE FROM Usuarios WHERE ID = %s"
    execute_query(query, (id_usuario,))

# ------------------------ FUNCIONÁRIOS ------------------------

def inserir_funcionario(nome, cargo, login, senha):
    query = '''
    INSERT INTO Funcionarios (Nome, Cargo, Login, Senha)
    VALUES (%s, %s, %s, %s)
    '''
    execute_query(query, (nome, cargo, login, senha))

def listar_funcionarios():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Funcionarios")
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def obter_funcionario(id_funcionario):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Funcionarios WHERE ID = %s", (id_funcionario,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

def atualizar_funcionario(id_funcionario, nome, cargo, login, senha):
    query = '''
    UPDATE Funcionarios
    SET Nome = %s, Cargo = %s, Login = %s, Senha = %s
    WHERE ID = %s
    '''
    execute_query(query, (nome, cargo, login, senha, id_funcionario))

def deletar_funcionario(id_funcionario):
    query = "DELETE FROM Funcionarios WHERE ID = %s"
    execute_query(query, (id_funcionario,))

# ------------------------ EMPRÉSTIMOS ------------------------

def inserir_emprestimo(id_livro, id_usuario, id_funcionario, data_emprestimo, data_devolucao, status):
    query = '''
    INSERT INTO Emprestimos (IDLivro, IDUsuario, IDFuncionario, DataEmprestimo, DataDevolucao, Status)
    VALUES (%s, %s, %s, %s, %s, %s)
    '''
    execute_query(query, (id_livro, id_usuario, id_funcionario, data_emprestimo, data_devolucao, status))

def listar_emprestimos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Emprestimos")
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def obter_emprestimo(id_emprestimo):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Emprestimos WHERE ID = %s", (id_emprestimo,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

def atualizar_emprestimo(id_emprestimo, id_livro, id_usuario, id_funcionario, data_emprestimo, data_devolucao, status):
    query = '''
    UPDATE Emprestimos
    SET IDLivro = %s, IDUsuario = %s, IDFuncionario = %s,
        DataEmprestimo = %s, DataDevolucao = %s, Status = %s
    WHERE ID = %s
    '''
    execute_query(query, (id_livro, id_usuario, id_funcionario, data_emprestimo, data_devolucao, status, id_emprestimo))

def deletar_emprestimo(id_emprestimo):
    query = "DELETE FROM Emprestimos WHERE ID = %s"
    execute_query(query, (id_emprestimo,))

# Funções para chamar as Views

def listar_livros_disponiveis():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM LivrosDisponiveis")
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def listar_historico_emprestimos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM HistoricoEmprestimos")
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def listar_emprestimos_vencidos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM EmprestimosVencidos")
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

# Funções para chamar as Procedures
def registrar_emprestimo(id_livro, id_usuario, id_funcionario, data_devolucao, data_emprestimo=None):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc('RegistrarEmprestimo', (id_livro, id_usuario, id_funcionario, data_devolucao, data_emprestimo))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def registrar_devolucao(id_emprestimo):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc('RegistrarDevolucao', (id_emprestimo,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()