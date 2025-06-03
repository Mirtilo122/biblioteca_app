-- Esse código não é usado e serve apenas para exemplo de CRUD das tabelas criadas.

-- CREATE (CRIAR)

-- Livros
INSERT INTO Livros (Titulo, Autor, Editora, Genero, Ano, ISBN, QuantidadeDisponivel) VALUES
('Dom Quixote', 'Miguel de Cervantes', 'Editora Clássica', 'Romance', 1605, '978-85-00-00001-1', 3),
('1984', 'George Orwell', 'Companhia das Letras', 'Ficção', 1949, '978-85-00-00002-2', 5),
('O Senhor dos Anéis', 'J.R.R. Tolkien', 'Martins Fontes', 'Fantasia', 1954, '978-85-00-00003-3', 2);

-- Usuarios
INSERT INTO Usuarios (Nome, Email, CPF, Telefone) VALUES
('Ana Silva', 'ana.silva@email.com', '123.456.789-00', '(11) 99999-0001'),
('João Souza', 'joao.souza@email.com', '987.654.321-00', '(11) 99999-0002');

-- Funcionarios
INSERT INTO Funcionarios (Nome, Cargo, Login, Senha) VALUES
('Carlos Mendes', 'Bibliotecário', 'carlos.m', 'senha123'),
('Luciana Alves', 'Assistente', 'luciana.a', 'senha456');

-- Emprestimos
INSERT INTO Emprestimos (IDLivro, IDUsuario, DataEmprestimo, DataDevolucao, Status) VALUES
(1, 1, '2025-05-01', '2025-05-15', 'devolvido'),
(2, 2, '2025-05-10', '2025-05-20', 'pendente');

-------------------------------------------------------

-- READ (LER)

SELECT * FROM Livros;
SELECT * FROM Usuarios;
SELECT * FROM Funcionarios;
SELECT * FROM Emprestimos;

-------------------------------------------------------

-- UPDATE (ATUALIZAR)

UPDATE Livros 
SET QuantidadeDisponivel = QuantidadeDisponivel - 1 
WHERE ID = 1;

UPDATE Usuarios 
SET Email = 'ana.silva@novomail.com' 
WHERE ID = 1;

UPDATE Funcionarios 
SET Cargo = 'Coordenador' 
WHERE ID = 1;

UPDATE Emprestimos 
SET Status = 'devolvido' 
WHERE ID = 2;

-------------------------------------------------------

-- DELETE (DELETAR)

DELETE FROM Livros 
WHERE ID = 3;

DELETE FROM Usuarios 
WHERE ID = 2;

DELETE FROM Funcionarios 
WHERE ID = 2;

DELETE FROM Emprestimos 
WHERE ID = 2;
