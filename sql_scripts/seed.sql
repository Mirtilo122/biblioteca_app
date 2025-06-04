USE bibliotecadb;

INSERT INTO Livros (Titulo, Autor, Editora, Genero, Ano, ISBN, QuantidadeDisponivel, ImagemURL)
VALUES 
('Dom Casmurro', 'Machado de Assis', 'Editora A', 'Romance', 1899, '1234567890123', 1, 'imgs\domcasmurro.jpg'),
('O Hobbit', 'J.R.R. Tolkien', 'Editora B', 'Fantasia', 1937, '9876543210987', 2, 'imgs\hobbit.jpg');

INSERT INTO Usuarios (Nome, Email, CPF, Telefone)
VALUES 
('João Silva', 'joao@gmail.com', '123.456.789-00', '11999998888'),
('Maria Souza', 'maria@gmail.com', '987.654.321-00', '11988887777');

INSERT INTO Funcionarios (Nome, Cargo, Login, Senha)
VALUES 
('Carlos Lima', 'Bibliotecário', 'carlos', '1234'),
('Ana Costa', 'Atendente', 'ana', 'abcd');

CALL RegistrarEmprestimo(2, 2, 2, '2025-05-10', '2025-05-01');
CALL RegistrarEmprestimo(1, 1, 2, '2025-05-30', '2025-05-21');
CALL RegistrarDevolucao(2);
CALL RegistrarEmprestimo(1, 2, 2, '2025-05-30', NULL);
