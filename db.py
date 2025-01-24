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
        CREATE TABLE IF NOT EXISTS Usuário (
            nome TEXT NOT NULL,
            senha TEXT NOT NULL,
            cpf BIGINT PRIMARY KEY,
            foto BYTEA
        )
    ''')

    connection.commit()

    return connection
    
def new_user(connection, name, cpf, password, photo):
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Usuário WHERE cpf=%s", 
                   (cpf,)
    )

    user = cursor.fetchone()

    if user:
        return False

    cursor.execute("INSERT INTO Usuário (nome, cpf, senha, foto) VALUES (%s, %s, %s, %s)", 
                   (name, cpf, password, photo)
    )

    connection.commit()

    return True

def log_in_user(connection, name, cpf, password):
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Usuário WHERE nome=%s AND cpf=%s AND senha=%s", 
                   (name, cpf, password)
    )

    connection.commit()

    user = cursor.fetchone()

    return user