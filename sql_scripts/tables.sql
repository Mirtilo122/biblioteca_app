CREATE DATABASE IF NOT EXISTS bibliotecadb;
USE bibliotecadb;

CREATE TABLE Livros (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Titulo VARCHAR(255) NOT NULL,
    Autor VARCHAR(255),
    Editora VARCHAR(255),
    Genero VARCHAR(100),
    Ano INT,
    ISBN VARCHAR(20),
    QuantidadeDisponivel INT
);

CREATE TABLE Usuarios (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(255),
    Email VARCHAR(255),
    CPF VARCHAR(14),
    Telefone VARCHAR(20)
);

CREATE TABLE Funcionarios (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(255),
    Cargo VARCHAR(100),
    Login VARCHAR(50),
    Senha VARCHAR(255)
);

CREATE TABLE Emprestimos (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    IDLivro INT,
    IDUsuario INT,
    IDFuncionario INT,
    DataEmprestimo DATE,
    DataDevolucao DATE,
    Status ENUM('pendente', 'devolvido'),
    FOREIGN KEY (IDLivro) REFERENCES Livros(ID),
    FOREIGN KEY (IDUsuario) REFERENCES Usuarios(ID),    
    FOREIGN KEY (IDFuncionario) REFERENCES Funcionarios(ID)
);