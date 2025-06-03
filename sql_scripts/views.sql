USE bibliotecadb;

-- Livros disponíveis para empréstimo
CREATE OR REPLACE VIEW LivrosDisponiveis AS
SELECT * FROM Livros
WHERE QuantidadeDisponivel > 0;

-- Histórico de empréstimos por usuário
CREATE OR REPLACE VIEW HistoricoEmprestimos AS
SELECT u.Nome AS Usuario, l.Titulo AS Livro, e.DataEmprestimo, e.DataDevolucao, e.Status
FROM Emprestimos e
JOIN Usuarios u ON e.IDUsuario = u.ID
JOIN Livros l ON e.IDLivro = l.ID;

-- Empréstimos vencidos (data de devolução menor que a atual e status "pendente")
CREATE OR REPLACE VIEW EmprestimosVencidos AS
SELECT e.*, u.Nome, l.Titulo
FROM Emprestimos e
JOIN Usuarios u ON e.IDUsuario = u.ID
JOIN Livros l ON e.IDLivro = l.ID
WHERE e.DataDevolucao < CURDATE() AND e.Status = 'pendente';
