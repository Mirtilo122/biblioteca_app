USE bibliotecadb;

-- Registrar Empréstimo
DELIMITER //

CREATE PROCEDURE RegistrarEmprestimo(
    IN p_IDLivro INT, 
    IN p_IDUsuario INT, 
    IN p_IDFuncionario INT, 
    IN p_DataDevolucao DATE, 
    IN p_DataEmprestimo DATE
)
BEGIN
    DECLARE v_DataEmprestimo DATE;
    IF p_DataEmprestimo IS NULL THEN
        SET v_DataEmprestimo = CURDATE();
    ELSE
        SET v_DataEmprestimo = p_DataEmprestimo;
    END IF;

    INSERT INTO Emprestimos (IDLivro, IDUsuario, IDFuncionario, DataEmprestimo, DataDevolucao, Status)
    VALUES (p_IDLivro, p_IDUsuario, p_IDFuncionario, v_DataEmprestimo, p_DataDevolucao, 'pendente');

    UPDATE Livros
    SET QuantidadeDisponivel = QuantidadeDisponivel - 1
    WHERE ID = p_IDLivro;
END //

-- Registrar Devolução
CREATE PROCEDURE RegistrarDevolucao(IN p_IDEmprestimo INT)
BEGIN
    DECLARE v_IDLivro INT;

    SELECT IDLivro INTO v_IDLivro FROM Emprestimos WHERE ID = p_IDEmprestimo;

    UPDATE Emprestimos
    SET Status = 'devolvido'
    WHERE ID = p_IDEmprestimo;

    UPDATE Livros
    SET QuantidadeDisponivel = QuantidadeDisponivel + 1
    WHERE ID = v_IDLivro;
END //

DELIMITER ;
