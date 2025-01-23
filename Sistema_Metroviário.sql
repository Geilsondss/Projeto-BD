-- Database: sistema metroviario

-- DROP DATABASE IF EXISTS "sistema metroviario";

CREATE DATABASE "sistema metroviario"
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Portuguese_Brazil.1252'
    LC_CTYPE = 'Portuguese_Brazil.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;


-- Tabela Cidade
CREATE TABLE Cidade (
    Cidade_Id INT PRIMARY KEY,
    Nome VARCHAR(50)
);

-- Tabela Estação
CREATE TABLE Estacao (
    Estacao_Id INT PRIMARY KEY,
    Localizacao VARCHAR(50),
    Nome VARCHAR(50),
    Cidade_Id INT,
    FOREIGN KEY (Cidade_Id) REFERENCES Cidade (Cidade_Id)
);

-- Tabela Empresa
CREATE TABLE Empresa (
    Empresa_Id INT PRIMARY KEY,
    Nome VARCHAR(50),
    Telefone VARCHAR(15)
);

-- Tabela Itinerário
CREATE TABLE Itinerario (
    Itinerario_Id INT PRIMARY KEY,
    Horario_saida TIME,
    Horario_chegada TIME,
    Funciona_Dias VARCHAR(50)
);

-- Tabela Trajeto
CREATE TABLE Trajeto (
    Trajeto_Id INT PRIMARY KEY,
    Origem VARCHAR(50),
    Destino VARCHAR(50)
);

-- Tabela Linha
CREATE TABLE Linha (
    Linha_Id INT PRIMARY KEY,
    Nome VARCHAR(50),
    IdEmpresa INT,
    IdTrajeto INT,
    FOREIGN KEY (IdEmpresa) REFERENCES Empresa (Empresa_Id),
    FOREIGN KEY (IdTrajeto) REFERENCES Trajeto (Trajeto_Id)
);

-- Tabela Metro
CREATE TABLE Metro (
    Metro_Id INT PRIMARY KEY,
    Capacidade INT,
    Modelo VARCHAR(50),
    IdEmpresa INT,
    FOREIGN KEY (IdEmpresa) REFERENCES Empresa (Empresa_Id)
);

-- Tabela Incidente
CREATE TABLE Incidente (
    Data DATE,
    Tipo VARCHAR(50),
    IdTrajeto INT,
    IdMetro INT,
    FOREIGN KEY (IdTrajeto) REFERENCES Trajeto (Trajeto_Id),
    FOREIGN KEY (IdMetro) REFERENCES Metro (Metro_Id)
);

-- Tabela Motorista
CREATE TABLE Motorista (
    Motorista_Id INT PRIMARY KEY,
    Nome VARCHAR(50),
    Foto BLOB,
    Contato VARCHAR(50),
    IdLinha INT,
    FOREIGN KEY (IdLinha) REFERENCES Linha (Linha_Id)
);

-- Tabela Passa_por
CREATE TABLE Passa_por (
    Estacao_Id INT,
    Linha_Id INT,
    PRIMARY KEY (Estacao_Id, Linha_Id),
    FOREIGN KEY (Estacao_Id) REFERENCES Estacao (Estacao_Id),
    FOREIGN KEY (Linha_Id) REFERENCES Linha (Linha_Id)
);

-- Tabela Usuario
CREATE TABLE Usuario (
    CPF VARCHAR(11) PRIMARY KEY,
    Nome VARCHAR(50),
    Senha VARCHAR(50),
    Foto BLOB
);

-- Tabela Realiza
CREATE TABLE Realiza (
    CPF VARCHAR(11),
    Trajeto_Id INT,
    PRIMARY KEY (CPF, Trajeto_Id),
    FOREIGN KEY (CPF) REFERENCES Usuario (CPF),
    FOREIGN KEY (Trajeto_Id) REFERENCES Trajeto (Trajeto_Id)
);

-- Tabela Possui
CREATE TABLE Possui (
    Itinerario_Id INT,
    Linha_Id INT,
    PRIMARY KEY (Itinerario_Id, Linha_Id),
    FOREIGN KEY (Itinerario_Id) REFERENCES Itinerario (Itinerario_Id),
    FOREIGN KEY (Linha_Id) REFERENCES Linha (Linha_Id)
);


-- Inserções na tabela Cidade
INSERT INTO Cidade (Cidade_Id, Nome) VALUES
(1001, 'Brasília'),
(1002, 'Taguatinga'),
(1003, 'Ceilândia'),
(1004, 'Águas Claras'),
(1005, 'Samambaia');

-- Inserções na tabela Estacao
INSERT INTO Estacao (Estacao_Id, Localizacao, Nome, Cidade_Id) VALUES
(2001, 'Plano Piloto', 'Estação Central', 1001),
(2002, 'Taguatinga Sul', 'Estação Praça do Relógio', 1002),
(2003, 'Ceilândia Centro', 'Estação Ceilândia Norte', 1003),
(2004, 'Águas Claras', 'Estação Águas Claras', 1004),
(2005, 'Samambaia Sul', 'Estação Terminal Samambaia', 1005);

-- Inserções na tabela Empresa
INSERT INTO Empresa (Empresa_Id, Nome, Telefone) VALUES
(3001, 'Metro DF', '(61) 3353-7373'),
(3002, 'Consórcio Central', '(61) 3555-8800'),
(3003, 'Metro Oeste', '(61) 3232-9900'),
(3004, 'Consórcio Sul', '(61) 3366-7700'),
(3005, 'Metro Nordeste', '(61) 3444-6600');

-- Inserções na tabela Itinerario
INSERT INTO Itinerario (Itinerario_Id, Horario_saida, Horario_chegada, Funciona_Dias) VALUES
(4001, '06:00:00', '07:30:00', 'Segunda a Sábado'),
(4002, '07:00:00', '09:00:00', 'Domingos e Feriados'),
(4003, '05:30:00', '08:00:00', 'Todos os dias'),
(4004, '10:15:00', '14:45:00', 'Segunda a Sexta'),
(4005, '20:45:00', '21:15:00', 'Todos os dias');

-- Inserções na tabela Trajeto
INSERT INTO Trajeto (Trajeto_Id, Origem, Destino) VALUES
(5001, 'Estação Central', 'Estação Praça do Relógio'),
(5002, 'Estação Ceilândia Norte', 'Estação Águas Claras'),
(5003, 'Estação Águas Claras', 'Estação Terminal Samambaia'),
(5004, 'Estação Praça do Relógio', 'Estação Central'),
(5005, 'Estação Terminal Samambaia', 'Estação Ceilândia Norte');

-- Inserções na tabela Linha
INSERT INTO Linha (Linha_Id, Nome, IdEmpresa, IdTrajeto) VALUES
(6001, 'Linha Verde', 3001, 5001),
(6002, 'Linha Azul', 3002, 5002),
(6003, 'Linha Laranja', 3003, 5003),
(6004, 'Linha Amarela', 3004, 5004),
(6005, 'Linha Roxa', 3005, 5005);

-- Inserções na tabela Metro
INSERT INTO Metro (Metro_Id, Capacidade, Modelo, IdEmpresa) VALUES
(7001, 320, 'Modelo BR-100', 3001),
(7002, 400, 'Modelo BR-200', 3002),
(7003, 300, 'Modelo BR-300', 3003),
(7004, 450, 'Modelo BR-400', 3004),
(7005, 350, 'Modelo BR-500', 3005);

-- Inserções na tabela Incidente
INSERT INTO Incidente (Data, Tipo, IdTrajeto, IdMetro) VALUES
('11-01-2025', 'Atraso técnico', 5001, 7001),
('01-02-2025', 'Superlotação', 5002, 7002),
('19-03-2025', 'Pane elétrica', 5003, 7003),
('23-04-2025', 'Interrupção programada', 5004, 7004),
('21-05-2025', 'Desvio operacional', 5005, 7005);

-- Inserções na tabela Motorista
INSERT INTO Motorista (Motorista_Id, Nome, Foto, Contato, IdLinha) VALUES
(8001, 'Carlos Almeida', NULL, '(61) 99999-1111', 6001),
(8002, 'Ana Beatriz', NULL, '(61) 98888-2222', 6002),
(8003, 'João Fernandes', NULL, '(61) 97777-3333', 6003),
(8004, 'Maria Clara', NULL, '(61) 96666-4444', 6004),
(8005, 'Pedro Henrique', NULL, '(61) 95555-5555', 6005);

-- Inserções na tabela Passa_por
INSERT INTO Passa_por (Estacao_Id, Linha_Id) VALUES
(2001, 6001),
(2002, 6001),
(2003, 6002),
(2004, 6002),
(2005, 6003);

-- Inserções na tabela Usuario
INSERT INTO Usuario (CPF, Nome, Senha, Foto) VALUES
('11111111111', 'Geilson Sa', 'senha1', NULL),
('22222222222', 'Wesley Oliveira', 'senha2', NULL),
('33333333333', 'Arthur Delpino', 'senha3', NULL),
('44444444444', Victor Fontes', 'senha4', NULL),
('55555555555', Maristela Holanda, 'senha5', NULL);

-- Inserções na tabela Realiza
INSERT INTO Realiza (CPF, Trajeto_Id) VALUES
('11111111111', 5001),
('22222222222', 5002),
('33333333333', 5003),
('44444444444', 5004),
('55555555555', 5005);

-- Inserções na tabela Possui
INSERT INTO Possui (Itinerario_Id, Linha_Id) VALUES
(4001, 6001),
(4002, 6002),
(4003, 6003),
(4004, 6004),
(4005, 6005);




