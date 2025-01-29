from tkinter import messagebox as message
import psycopg2

def create_tables():
    connection = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="HashMap1990",
        host="localhost",
        port="5432"
    )

    cursor = connection.cursor()

    cursor.execute('''
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
            Trajeto_Id SERIAL PRIMARY KEY,
            Origem VARCHAR(50),
            Destino VARCHAR(50)
        );

        -- Tabela Linha
        CREATE TABLE IF NOT EXISTS Linha (
            Linha_Id INT PRIMARY KEY,
            Nome VARCHAR(50),
            IdEmpresa INT,
            IdTrajeto INT,
            FOREIGN KEY (IdEmpresa) REFERENCES Empresa (Empresa_Id),
            FOREIGN KEY (IdTrajeto) REFERENCES Trajeto (Trajeto_Id) ON DELETE CASCADE
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
            IdTrajeto INT,
            IdMetro INT,
            FOREIGN KEY (IdTrajeto) REFERENCES Trajeto (Trajeto_Id) ON DELETE CASCADE,
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
            Estacao_Id INT,
            Linha_Id INT,
            PRIMARY KEY (Estacao_Id, Linha_Id),
            FOREIGN KEY (Estacao_Id) REFERENCES Estacao (Estacao_Id),
            FOREIGN KEY (Linha_Id) REFERENCES Linha (Linha_Id)
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
            Trajeto_Id INT,
            PRIMARY KEY (CPF, Trajeto_Id),
            FOREIGN KEY (CPF) REFERENCES Usuario (CPF) ON DELETE CASCADE,
            FOREIGN KEY (Trajeto_Id) REFERENCES Trajeto (Trajeto_Id) ON DELETE CASCADE
        );

        -- Tabela Possui
        CREATE TABLE IF NOT EXISTS Possui (
            Itinerario_Id INT,
            Linha_Id INT,
            PRIMARY KEY (Itinerario_Id, Linha_Id),
            FOREIGN KEY (Itinerario_Id) REFERENCES Itinerario (Itinerario_Id),
            FOREIGN KEY (Linha_Id) REFERENCES Linha (Linha_Id) ON DELETE CASCADE
        );
                   
        CREATE VIEW Cidades_visitadas AS
        SELECT c.nome AS cidade
        FROM Usuario u
        JOIN Realiza r ON u.cpf = r.cpf
        JOIN Trajeto t ON r.trajeto_id = t.trajeto_id
        JOIN Linha l ON l.idTrajeto = t.Trajeto_id
        JOIN Passar_Por p ON p.linha_id = l.linha_id
        JOIN Estação e ON e.estacao_id = p.estacao_id
        JOIN Cidade c ON c.cidade_id = e.cidade_id
        WHERE u.CPF = :cpf;
    ''')

    connection.commit()

    return connection

def log_in(connection, name, cpf, password):
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Usuario WHERE nome=%s AND cpf=%s AND senha=%s", 
                   (name, cpf, password)
    )

    connection.commit()

    user = cursor.fetchone()

    return user

def new_user(connection, name, cpf, password, photo):
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Usuario WHERE cpf=%s", 
                   (cpf,)
    )

    user = cursor.fetchone()

    if user:
        return True

    cursor.execute("INSERT INTO Usuario (nome, cpf, senha, foto) VALUES (%s, %s, %s, %s)", 
                   (name, cpf, password, photo)
    )

    connection.commit()

    return False

def update_user(connection, cpf, new_name, new_cpf, new_password, new_photo):
    cursor = connection.cursor()

    cursor.execute("UPDATE Usuario SET nome=%s, cpf=%s, senha=%s, foto=%s WHERE cpf=%s", 
                   (new_name, new_cpf, new_password, new_photo, cpf)
    )

    cursor.execute("SELECT * FROM Usuario WHERE cpf=%s", 
                   (new_cpf,)
    )

    connection.commit()

    user = cursor.fetchone()

    return user

def delete_user(connection, cpf):
    cursor = connection.cursor()

    cursor.execute("DELETE FROM Usuario WHERE cpf=%s", 
                   (cpf,)
    )

    connection.commit()

def get_my_paths(connection, cpf):
    cursor = connection.cursor()

    cursor.execute("SELECT t.* FROM Trajeto t JOIN Realiza r ON t.trajeto_id = r.trajeto_id WHERE r.cpf = %s",
                   (cpf,)
    )

    connection.commit()

    paths = cursor.fetchall()

    return paths

def get_not_my_paths(connection, cpf):
    cursor = connection.cursor()

    cursor.execute("SELECT t.* FROM Trajeto t JOIN Realiza r ON t.trajeto_id = r.trajeto_id WHERE r.cpf != %s",
                   (cpf,)
    )

    paths = cursor.fetchall()

    return paths

def new_path(connection, origin, destination, cpf):
    cursor = connection.cursor()

    cursor.execute("INSERT INTO Trajeto (Origem, Destino) VALUES (%s, %s) RETURNING Trajeto_Id",
                   (origin, destination)
    )

    id = cursor.fetchone()[0]

    assign_path(connection, id, cpf)

def assign_path(connection, path, cpf):
    cursor = connection.cursor()

    cursor.execute("INSERT INTO Realiza (CPF, Trajeto_Id) VALUES (%s, %s)", 
                   (cpf, path)
    )

    connection.commit()

def update_path(connection, origin, destination, path):
    cursor = connection.cursor()

    cursor.execute("UPDATE Trajeto SET Origem=%s, Destino=%s WHERE Trajeto_Id=%s", 
                   (origin, destination, path)
    )

    connection.commit()

def delete_path(connection, path):
    cursor = connection.cursor()

    cursor.execute("DELETE FROM Trajeto WHERE Trajeto_Id=%s", 
                   (path,)
    )

    connection.commit()