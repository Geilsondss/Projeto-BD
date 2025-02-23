-- Tabela Cidade
CREATE TABLE IF NOT EXISTS Cidade (
    Cidade_Id INT PRIMARY KEY,
    Nome VARCHAR(50)
);

-- Tabela Estação
CREATE TABLE IF NOT EXISTS Estacao (
    Estacao_Id INT PRIMARY KEY,
    Localizacao VARCHAR(50),
    Nome VARCHAR(50),
    Cidade_Id INT,
    FOREIGN KEY (Cidade_Id) REFERENCES Cidade (Cidade_Id)
);

-- Tabela Empresa
CREATE TABLE IF NOT EXISTS Empresa (
    Empresa_Id INT PRIMARY KEY,
    Nome VARCHAR(50),
    Telefone VARCHAR(15)
);

-- Tabela Itinerário
CREATE TABLE IF NOT EXISTS Itinerario (
    Itinerario_Id INT PRIMARY KEY,
    Horario_saida TIME,
    Horario_chegada TIME,
    Funciona_Dias VARCHAR(50)
);

-- Tabela Trajeto
CREATE TABLE IF NOT EXISTS Trajeto (
    Origem INT,
    Destino INT,
    PRIMARY KEY (Origem, Destino),
    FOREIGN KEY (Origem) REFERENCES Estacao (Estacao_Id),
    FOREIGN KEY (Destino) REFERENCES Estacao (Estacao_Id),
    CONSTRAINT different CHECK (Origem <> Destino)
);

-- Tabela Linha
CREATE TABLE IF NOT EXISTS Linha (
    Linha_Id SERIAL PRIMARY KEY,
    Nome VARCHAR(50),
    IdEmpresa INT,
    Origem INT,
    Destino INT,
    FOREIGN KEY (IdEmpresa) REFERENCES Empresa (Empresa_Id),
    FOREIGN KEY (Origem, Destino) REFERENCES Trajeto (Origem, Destino) ON DELETE CASCADE
);

-- Tabela Metro
CREATE TABLE IF NOT EXISTS Metro (
    Metro_Id INT PRIMARY KEY,
    Capacidade INT,
    Modelo VARCHAR(50),
    IdEmpresa INT,
    FOREIGN KEY (IdEmpresa) REFERENCES Empresa (Empresa_Id)
);

-- Tabela Incidente
CREATE TABLE IF NOT EXISTS Incidente (
    Data DATE,
    Tipo VARCHAR(50),
    Origem INT,
    Destino INT,
    IdMetro INT,
    PRIMARY KEY (Origem, Destino, IdMetro),
    FOREIGN KEY (Origem, Destino) REFERENCES Trajeto (Origem, Destino) ON DELETE CASCADE,
    FOREIGN KEY (IdMetro) REFERENCES Metro (Metro_Id)
);

-- Tabela Motorista
CREATE TABLE IF NOT EXISTS Motorista (
    Motorista_Id INT PRIMARY KEY,
    Nome VARCHAR(50),
    Foto BYTEA,
    Contato VARCHAR(50),
    IdLinha INT,
    FOREIGN KEY (IdLinha) REFERENCES Linha (Linha_Id) ON DELETE CASCADE
);

-- Tabela Passa_por
CREATE TABLE IF NOT EXISTS Passa_por (
    Origem INT,
    Destino INT,
    Linha_Id INT,
    PRIMARY KEY (Origem, Destino, Linha_Id),
    FOREIGN KEY (Origem) REFERENCES Estacao (Estacao_Id),
    FOREIGN KEY (Destino) REFERENCES Estacao (Estacao_Id),
    FOREIGN KEY (Linha_Id) REFERENCES Linha (Linha_Id) ON DELETE CASCADE
);

-- Tabela Usuario
CREATE TABLE IF NOT EXISTS Usuario (
    CPF VARCHAR(11) PRIMARY KEY,
    Nome VARCHAR(50),
    Senha VARCHAR(50),
    Foto BYTEA
);

-- Tabela Realiza
CREATE TABLE IF NOT EXISTS Realiza (
    CPF VARCHAR(11),
    Origem INT,
    Destino INT,
    PRIMARY KEY (CPF, Origem, Destino),
    FOREIGN KEY (CPF) REFERENCES Usuario (CPF) ON DELETE CASCADE,
    FOREIGN KEY (Origem, Destino) REFERENCES Trajeto (Origem, Destino) ON DELETE CASCADE
);

-- Tabela Possui
CREATE TABLE IF NOT EXISTS Possui (
    Itinerario_Id INT,
    Linha_Id INT,
    PRIMARY KEY (Itinerario_Id, Linha_Id),
    FOREIGN KEY (Itinerario_Id) REFERENCES Itinerario (Itinerario_Id),
    FOREIGN KEY (Linha_Id) REFERENCES Linha (Linha_Id) ON DELETE CASCADE
);

CREATE OR REPLACE VIEW Linhas_Completas AS 
SELECT 
    l.linha_id,
    l.nome AS Nome_Linha,
    e.empresa_id,
    e.nome AS Nome_Empresa,
    s1.estacao_id AS Id_Origem,
    s1.nome AS Nome_Origem,
    s2.estacao_id AS Id_Destino,
    s2.nome AS Nome_Destino
FROM Linha l
JOIN Empresa e ON e.empresa_id = l.idempresa
JOIN Passa_Por p ON p.linha_id = l.linha_id
JOIN Estacao s1 ON s1.estacao_id = p.origem
JOIN Estacao s2 ON s2.estacao_id = p.destino; 
            
CREATE OR REPLACE PROCEDURE Inserção_Linha (route TEXT, corp INT, origin INT, destination INT)
AS $$
DECLARE
    current_route Linha%ROWTYPE;
    new_route INT;
    path Trajeto%ROWTYPE;
BEGIN
    SELECT * INTO current_route FROM Linha WHERE Nome=route LIMIT 1;
    IF current_route.Nome IS NULL THEN
        SELECT * INTO path FROM Trajeto WHERE Origem=origin AND Destino=destination LIMIT 1;
        IF path.Origem IS NULL THEN
            INSERT INTO Trajeto (Origem, Destino) VALUES (origin, destination);
        END IF;
        INSERT INTO Linha (Nome, idEmpresa, Origem, Destino) VALUES (route, corp, origin, destination) RETURNING Linha_Id INTO new_route;
        INSERT INTO Passa_Por (Linha_Id, Origem, Destino) VALUES (new_route, origin, destination);
    END IF;
END;
$$ LANGUAGE plpgsql;
            
CREATE OR REPLACE FUNCTION Trajetos_Completos (user_cpf VARCHAR(11), mine BOOLEAN)
RETURNS TABLE (
    idOrigem INT, 
    nomeOrigem VARCHAR(50),
    idDestino INT,
    nomeDestino VARCHAR(50)
) AS $$
DECLARE
    query TEXT;
BEGIN
    IF mine THEN
        query := 'SELECT 
                    s1.estacao_id,
                    s1.nome,
                    s2.estacao_id,
                    s2.nome
                FROM Realiza r
                JOIN Trajeto t ON t.origem = r.origem AND t.destino = r.destino
                JOIN Estacao s1 ON s1.estacao_id = t.origem
                JOIN Estacao s2 ON s2.estacao_id = t.destino
                WHERE r.cpf = $1';
    ELSE
        query := 'SELECT 
                    s1.estacao_id,
                    s1.nome,
                    s2.estacao_id,
                    s2.nome
                FROM Trajeto t
                JOIN Estacao s1 ON s1.estacao_id = t.origem
                JOIN Estacao s2 ON s2.estacao_id = t.destino
                WHERE NOT EXISTS (
                    SELECT 1
                    FROM Realiza r
                    WHERE r.cpf = $1
                    AND t.origem = r.origem
                    AND t.destino = r.destino
                )';
    END IF;

    RETURN QUERY EXECUTE query USING user_cpf;
END;    
$$ LANGUAGE plpgsql;  

CREATE OR REPLACE FUNCTION Deletar_BD ()
RETURNS void
AS $$
DECLARE 
    record RECORD;
BEGIN
    FOR record IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
        EXECUTE 'DROP TABLE IF EXISTS public.' || record.tablename || ' CASCADE';
    END LOOP;
END;
$$ LANGUAGE plpgsql;   

DO $$
BEGIN 
    IF NOT EXISTS (SELECT 1 FROM Usuario) THEN
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
        INSERT INTO Trajeto (Origem, Destino) VALUES
        (2001, 2002),
        (2003, 2004),
        (2004, 2005),
        (2002, 2001),
        (2005, 2003);

        -- Inserções na tabela Linha
        INSERT INTO Linha (Linha_Id, Nome, IdEmpresa, Origem, Destino) VALUES
        (6001, 'Linha Verde', 3001, 2001, 2002),
        (6002, 'Linha Azul', 3002, 2003, 2004),
        (6003, 'Linha Laranja', 3003, 2004, 2005),
        (6004, 'Linha Amarela', 3004, 2002, 2001),
        (6005, 'Linha Roxa', 3005, 2005, 2003);

        -- Inserções na tabela Metro
        INSERT INTO Metro (Metro_Id, Capacidade, Modelo, IdEmpresa) VALUES
        (7001, 320, 'Modelo BR-100', 3001),
        (7002, 400, 'Modelo BR-200', 3002),
        (7003, 300, 'Modelo BR-300', 3003),
        (7004, 450, 'Modelo BR-400', 3004),
        (7005, 350, 'Modelo BR-500', 3005);

        -- Inserções na tabela Incidente
        INSERT INTO Incidente (Data, Tipo, Origem, Destino, IdMetro) VALUES
        ('11-01-2025', 'Atraso técnico', 2001, 2002, 7001),
        ('01-02-2025', 'Superlotação', 2003, 2004, 7002),
        ('19-03-2025', 'Pane elétrica', 2004, 2005, 7003),
        ('23-04-2025', 'Interrupção programada', 2002, 2001, 7004),
        ('21-05-2025', 'Desvio operacional', 2005, 2003, 7005);

        -- Inserções na tabela Motorista
        INSERT INTO Motorista (Motorista_Id, Nome, Foto, Contato, IdLinha) VALUES
        (8001, 'Carlos Almeida', NULL, '(61) 99999-1111', 6001),
        (8002, 'Ana Beatriz', NULL, '(61) 98888-2222', 6002),
        (8003, 'João Fernandes', NULL, '(61) 97777-3333', 6003),
        (8004, 'Maria Clara', NULL, '(61) 96666-4444', 6004),
        (8005, 'Pedro Henrique', NULL, '(61) 95555-5555', 6005);

        -- Inserções na tabela Passa_por
        INSERT INTO Passa_por (Origem, Destino, Linha_Id) VALUES
        (2001, 2002, 6001),
        (2003, 2004, 6002),
        (2004, 2005, 6003),
        (2002, 2001, 6004),
        (2005, 2003, 6005);

        -- Inserções na tabela Usuario
        INSERT INTO Usuario (CPF, Nome, Senha, Foto) VALUES
        ('11111111111', 'Geilson Sa', 'senha1', NULL),
        ('22222222222', 'Wesley Oliveira', 'senha2', NULL),
        ('33333333333', 'Arthur Delpino', 'senha3', NULL),
        ('44444444444', 'Victor Fontes', 'senha4', NULL),
        ('55555555555', 'Maristela Holanda', 'senha5', NULL);

        -- Inserções na tabela Realiza
        INSERT INTO Realiza (CPF, Origem, Destino) VALUES
        ('11111111111', 2001, 2002),
        ('22222222222', 2003, 2004),
        ('33333333333', 2004, 2005),
        ('44444444444', 2002, 2001),
        ('55555555555', 2005, 2003);

        -- Inserções na tabela Possui
        INSERT INTO Possui (Itinerario_Id, Linha_Id) VALUES
        (4001, 6001),
        (4002, 6002),
        (4003, 6003),
        (4004, 6004),
        (4005, 6005);
    END IF;
END $$