import tkinter
import io

from PIL import Image as Photo, ImageTk as PhotoTk
from tkinter import messagebox as message
from tkinter import filedialog as file
from db import *

connection = create_tables()

def check_cpf(char, size):
    return char.isdigit() and len(size) <= 11

def to_blob(path):
    photo = Photo.open(path)
    photo = photo.resize((100, 100)) 

    photo_blob = io.BytesIO()
    photo.save(photo_blob, 'PNG')

    return photo_blob.getvalue()

def sign_up():
    name = name_field.get()
    cpf = cpf_field.get()
    password = password_field.get()
    
    if not name or not password or not cpf:
        message.showwarning("Erro", "Preencha todos os campos")
        return
    
    if len(cpf) < 11:
        message.showwarning("Erro", "Preencha um CPF válido")
        return

    if path.get():
        photo = to_blob(path.get())
    else:
        photo = None
    
    if not new_user(connection, name, cpf, password, photo):
        message.showwarning("Erro", "CPF fornecido já utilizado")
        return

    message.showinfo("Sucesso", "Usuário registrado com sucesso")

    name_field.delete(0, tkinter.END)
    cpf_field.delete(0, tkinter.END)
    password_field.delete(0, tkinter.END)
    path.set(str())
    photo_panel.config(image=str())
    photo_panel.image = str()

def log_in():
    name = name_field.get()
    cpf = cpf_field.get()
    password = password_field.get()
    
    if not name or not password or not cpf:
        message.showwarning("Erro", "Preencha todos os campos")
        return
    
    if len(cpf) < 11:
        message.showwarning("Erro", "Preencha um CPF válido")
        return
    
    user = log_in_user(connection, name, cpf, password)
    
    if user:
        screen.destroy()

        login_screen = tkinter.Tk()
        login_screen.title("Menu")
        
        welcome_label = tkinter.Label(login_screen, text="Olá, " + name)
        welcome_label.pack(padx=20, pady=20)

        login_screen.mainloop()
    else:
        message.showerror("Erro", "Nome, senha ou CPF inválidos")

    name_field.delete(0, tkinter.END)
    cpf_field.delete(0, tkinter.END)
    password_field.delete(0, tkinter.END)
    path.set(str())
    photo_panel.config(image=str())
    photo_panel.image = str()

def search_photo():
    photo = file.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    path.set(photo)
    
    if photo:
        photo = Photo.open(photo)
        photo = photo.resize((100, 100))

        photo = PhotoTk.PhotoImage(photo)

        photo_panel.config(image=photo)
        photo_panel.image = photo


# Main
screen = tkinter.Tk()
screen.title("Sistema Metroviário")

path = tkinter.StringVar()

width = screen.winfo_screenwidth()
height = screen.winfo_screenheight()

width = (width // 2) - (240 // 2)
height = (height // 2) - (240 // 2)

screen.geometry(f"{260}x{300}+{width}+{height}")


# Labels
name_label = tkinter.Label(screen, text="Nome:")
name_label.grid(row=0, column=0, padx=10, pady=10)

cpf_label = tkinter.Label(screen, text="CPF:")
cpf_label.config(text=cpf_label.cget("text")[:11])
cpf_label.grid(row=1, column=0, padx=10, pady=10)

password_label = tkinter.Label(screen, text="Senha:")
password_label.grid(row=2, column=0, padx=10, pady=10)

photo_panel = tkinter.Label(screen)
photo_panel.grid(row=6, column=1, padx=10, pady=10)


# Fields
name_field = tkinter.Entry(screen)
name_field.grid(row=0, column=1, padx=10, pady=10)

validation = (screen.register(check_cpf), '%S', '%P')
cpf_field = tkinter.Entry(screen, validate='key', validatecommand=validation)
cpf_field.grid(row=1, column=1, padx=10, pady=10)

password_field = tkinter.Entry(screen, show="*")
password_field.grid(row=2, column=1, padx=10, pady=10)


# Buttons
login_button = tkinter.Button(screen, text="Log-in", command=log_in)
login_button.grid(row=3, column=0, padx=10, pady=10)

sign_up_button = tkinter.Button(screen, text="Cadastrar", command=sign_up)
sign_up_button.grid(row=3, column=1, padx=10, pady=10)

photo_button = tkinter.Button(screen, text="Escolher foto", command=search_photo)
photo_button.grid(row=6, column=0, padx=10, pady=10)

screen.mainloop()

connection.close()