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

    with open('db.sql', 'r', encoding='utf-8') as file:
        sql = file.read()

    cursor.execute(sql)

    connection.commit()

    return connection

def log_in(connection, name, cpf, password):
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Usuario WHERE nome=%s AND cpf=%s AND senha=%s", 
                   (name, cpf, password)
    )

    user = cursor.fetchone()

    return user

def sign_up(connection, name, cpf, password, photo):
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Usuario WHERE cpf=%s", 
                   (cpf,)
    )

    if cursor.fetchone():
        return False

    cursor.execute("INSERT INTO Usuario (nome, cpf, senha, foto) VALUES (%s, %s, %s, %s)", 
                   (name, cpf, password, photo)
    )

    connection.commit()

    return True

def update_user(connection, cpf, new_name, new_password, new_photo):
    cursor = connection.cursor() 

    cursor.execute("UPDATE Usuario SET nome=%s, senha=%s, foto=%s WHERE cpf=%s", 
                   (new_name, new_password, new_photo, cpf)
    )

    cursor.execute("SELECT * FROM Usuario WHERE cpf=%s", 
                   (cpf,)
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

def get_paths(connection, cpf, mine):
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Trajetos_Completos(%s, %s)",
                (cpf, mine)
    )

    paths = cursor.fetchall()

    return paths

def new_path(connection, origin, destination, cpf):
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Trajeto WHERE Origem=%s AND Destino=%s",
                   (origin, destination)
    )

    if cursor.fetchone():
        return False

    cursor.execute("INSERT INTO Trajeto (Origem, Destino) VALUES (%s, %s)",
                   (origin, destination)
    )

    connection.commit()

    assign_path(connection, origin, destination, cpf)

    return True

def assign_path(connection, origin, destination, cpf):
    cursor = connection.cursor()

    cursor.execute("INSERT INTO Realiza (CPF, Origem, Destino) VALUES (%s, %s, %s)", 
                   (cpf, origin, destination)
    )

    connection.commit()

def update_path(connection, origin, destination, cpf, new_origin, new_destination):
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Realiza WHERE CPF=%s AND Origem=%s AND Destino=%s",
                   (cpf, new_origin, new_destination)
    )

    if cursor.fetchone() and not (origin == new_origin and destination == new_destination):
        return False

    cursor.execute("INSERT INTO Trajeto (Origem, Destino) VALUES (%s, %s) ON CONFLICT (Origem, Destino) DO NOTHING",
                (new_origin, new_destination)
    )

    cursor.execute("UPDATE Realiza SET Origem=%s, Destino=%s WHERE CPF=%s AND Origem=%s AND Destino=%s", 
                   (new_origin, new_destination, cpf, origin, destination)
    )

    connection.commit()

    return True

def unassign_path(connection, cpf, origin, destination):
    cursor = connection.cursor()

    cursor.execute("DELETE FROM Realiza WHERE CPF=%s AND Origem=%s AND Destino=%s", 
                   (cpf, origin, destination)
    )

    connection.commit()

def delete_path(connection, origin, destination):
    cursor = connection.cursor()

    cursor.execute("DELETE FROM Trajeto WHERE Origem=%s AND Destino=%s", 
                   (origin, destination)
    )

    connection.commit()

def get_corps(connection):
    cursor = connection.cursor()

    cursor.execute("SELECT DISTINCT * FROM Empresa",
                   ()
    )

    corps = cursor.fetchall()

    return corps

def get_stations(connection):
    cursor = connection.cursor()

    cursor.execute("SELECT DISTINCT * FROM Estacao",
                   ()
    )

    stations = cursor.fetchall()

    return stations

def get_routes(connection):
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Linhas_Completas",
                   ()
    )

    routes = cursor.fetchall()

    return routes

def new_route(connection, route, corp, origin, destination):
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Linha WHERE nome=%s",
                    (route,)               
    )

    if cursor.fetchone():
        return False
        
    cursor.execute("CALL Inserção_Linha (%s, %s, %s, %s)",
                    (route, corp, origin, destination)
    )

    connection.commit()

    return True

def update_route(connection, route, old_name, old_origin, old_destination, new_name, new_corp, new_origin, new_destination):
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Linha WHERE Nome=%s",
                    (new_name,)
    )

    if cursor.fetchone() and not (old_name == new_name):
        return False

    cursor.execute("INSERT INTO Trajeto (Origem, Destino) VALUES (%s, %s) ON CONFLICT (Origem, Destino) DO NOTHING",
                   (new_origin, new_destination)
    )

    cursor.execute("UPDATE Linha SET Nome=%s, idEmpresa=%s, Origem=%s, Destino=%s WHERE Linha_Id=%s", 
                   (new_name, new_corp, new_origin, new_destination, route)
    )

    cursor.execute("UPDATE Passa_Por SET Origem=%s, Destino=%s WHERE Linha_Id=%s AND Origem=%s AND Destino=%s", 
                   (new_origin, new_destination, route, old_origin, old_destination)
    )

    connection.commit()

    return True

def delete_route(connection, route):
    cursor = connection.cursor()

    cursor.execute("DELETE FROM Linha WHERE Linha_Id=%s", 
                   (route,)
    )

    connection.commit()