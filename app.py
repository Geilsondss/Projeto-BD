import tkinter
import io
import db

from PIL import Image as Photo, ImageTk as PhotoTk
from tkinter import messagebox as message
from tkinter import filedialog as file
from tkinter import ttk


connection = db.create_tables()

def check_cpf(char, size):
    return char.isdigit() and len(size) <= 11

def to_blob(path):
    if path.get():
        photo = Photo.open(path.get())
        photo = photo.resize((100, 100)) 

        photo_blob = io.BytesIO()
        photo.save(photo_blob, 'PNG')

        return photo_blob.getvalue()
    return None

def set_geometry(screen, new_width, new_height):
    width = screen.winfo_screenwidth()
    height = screen.winfo_screenheight()

    width = (width // 2) - (new_width // 2)
    height = (height // 2) - (new_height // 2)

    screen.geometry(f"{new_width}x{new_height}+{width}+{height}")

def search_photo(photo_panel, photo=None, path=None):   
    if path:
        dir = file.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if dir:
            path = dir

            photo = Photo.open(dir)
            photo = photo.resize((100, 100))

            photo = PhotoTk.PhotoImage(photo)

            photo_panel.config(image=photo)
            photo_panel.image = photo
    else:
        if photo:
            photo = Photo.open(io.BytesIO(photo))

            photo = PhotoTk.PhotoImage(photo)

            photo_panel.config(image=photo)
            photo_panel.image = photo










def main():
    main_screen = tkinter.Tk()
    main_screen.title("Sistema Metroviário")

    path = tkinter.StringVar() # Path to photo

    set_geometry(main_screen, 260, 300)


    ### Functions ###
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
        
        user = db.log_in(connection, name, cpf, password)
        
        if user:
            main_screen.destroy()
            home(user)
        else:
            message.showerror("Erro", "Nome, senha ou CPF inválidos")
            password_field.delete(0, tkinter.END)

    def sign_up():
        name = name_field.get()
        cpf = cpf_field.get()
        password = password_field.get()
        photo = to_blob(path)

        if not name or not password or not cpf:
            message.showwarning("Erro", "Preencha todos os campos")
            return
        
        if len(cpf) < 11:
            message.showwarning("Erro", "Preencha um CPF válido")
            return

        if db.new_user(connection, name, cpf, password, photo):
            message.showwarning("Erro", "CPF fornecido já utilizado")
            return

        message.showinfo("Sucesso", "Usuário registrado com sucesso")

        name_field.delete(0, tkinter.END)
        cpf_field.delete(0, tkinter.END)
        password_field.delete(0, tkinter.END)
        path.set(str())
        photo_panel.config(image=str())
        photo_panel.image = str()

    ### Labels ###
    name_label = tkinter.Label(main_screen, text="Nome:")
    name_label.grid(row=0, column=0, padx=10, pady=10)

    cpf_label = tkinter.Label(main_screen, text="CPF:")
    cpf_label.config(text=cpf_label.cget("text")[:11]) # Length limiter
    cpf_label.grid(row=1, column=0, padx=10, pady=10)

    password_label = tkinter.Label(main_screen, text="Senha:")
    password_label.grid(row=2, column=0, padx=10, pady=10)

    photo_panel = tkinter.Label(main_screen)
    photo_panel.grid(row=6, column=1, padx=10, pady=10)


    ### Fields ###
    name_field = tkinter.Entry(main_screen)
    name_field.grid(row=0, column=1, padx=10, pady=10)

    validation = (main_screen.register(check_cpf), '%S', '%P') # Check if it is less than 12 digits long
    cpf_field = tkinter.Entry(main_screen, validate='key', validatecommand=validation)
    cpf_field.grid(row=1, column=1, padx=10, pady=10)

    password_field = tkinter.Entry(main_screen, show="*")
    password_field.grid(row=2, column=1, padx=10, pady=10)


    ### Buttons ###
    login_button = tkinter.Button(main_screen, text="Log-in", command=lambda: log_in())
    login_button.grid(row=3, column=0, padx=10, pady=10)

    sign_up_button = tkinter.Button(main_screen, text="Cadastrar", command=lambda: sign_up())
    sign_up_button.grid(row=3, column=1, padx=10, pady=10)

    photo_button = tkinter.Button(main_screen, text="Escolher foto", command=lambda: search_photo(photo_panel, None, path))
    photo_button.grid(row=6, column=0, padx=10, pady=10)

    main_screen.mainloop()

    connection.close()

def home(user):
    home_screen = tkinter.Tk()
    home_screen.title("Menu")

    set_geometry(home_screen, 720, 480)

    paths = db.get_my_paths(connection, user[0])
    

    ### Labels ###
    welcome_label = tkinter.Label(home_screen, text="Olá, " + user[1] + "!")
    welcome_label.grid(row=1, column=0, padx=20, pady=20)

    paths_label = tkinter.Label(home_screen, text="Seus trajetos:")
    paths_label.grid(row=2, column=0, padx=20, pady=20)


    ### Panels ###
    photo_panel = tkinter.Label(home_screen)
    photo_panel.grid(row=0, column=0, padx=10, pady=10)
    search_photo(photo_panel, user[3])


    ### Buttons ###
    change_button = tkinter.Button(home_screen, text="Alterar", command=lambda: update_user(home_screen, user))
    change_button.grid(row=1, column=1, padx=10, pady=10)

    delete_button = tkinter.Button(home_screen, text="Excluir", command=lambda: delete_user(home_screen, user[0]))
    delete_button.grid(row=1, column=2, padx=10, pady=10)

    paths_button = tkinter.Button(home_screen, text="Adicionar", command=lambda: assign_path(home_screen, user))
    paths_button.grid(row=2, column=1, padx=10, pady=10)


    ### Scroll Frame ###
    frame = tkinter.Frame(home_screen)
    frame.grid(row=3, column=0, columnspan=6, padx=10, pady=10)

    canvas = tkinter.Canvas(frame)
    canvas.grid(row=0, column=0, sticky="nsew")

    scroll = tkinter.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scroll.grid(row=0, column=1, sticky="ns")

    canvas.config(yscrollcommand=scroll.set)

    user_frame = tkinter.Frame(canvas)
    canvas.create_window((0, 0), window=user_frame, anchor="nw")

    for i, path in enumerate(paths):
        path_label = tkinter.Label(user_frame, text=f"Origem: {path[1]} - Destino: {path[2]}")
        path_label.grid(row=i, column=2, padx=10, pady=5, sticky="w")

        path_change_button = tkinter.Button(user_frame, text="Alterar", command=lambda: change_path(home_screen, path[0], user))
        path_change_button.grid(row=i, column=0, padx=10, pady=5, sticky="w")

        path_delete_button = tkinter.Button(user_frame, text="Excluir", command=lambda: delete_path(home_screen, user, path[0]))
        path_delete_button.grid(row=i, column=1, padx=10, pady=5, sticky="w")

    user_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    home_screen.mainloop()

def update_user(screen, user):
    screen.destroy()

    update_screen = tkinter.Tk()
    update_screen.title("Alterar usuário")

    path = tkinter.StringVar()

    set_geometry(update_screen, 260, 300)


    ### Functions ###
    def update():
        new_user = db.update_user(connection, user[0], name_field.get(), cpf_field.get(), password_field.get(), to_blob(path))
        update_screen.destroy()
        home(new_user)

    def cancel():
        update_screen.destroy()
        home(user)


    ### Labels ###
    name_label = tkinter.Label(update_screen, text="Nome:")
    name_label.grid(row=0, column=0, padx=10, pady=10)

    cpf_label = tkinter.Label(update_screen, text="CPF:")
    cpf_label.config(text=cpf_label.cget("text")[:11])
    cpf_label.grid(row=1, column=0, padx=10, pady=10)

    password_label = tkinter.Label(update_screen, text="Senha:")
    password_label.grid(row=2, column=0, padx=10, pady=10)


    ### Panels ###
    photo_panel = tkinter.Label(update_screen)
    photo_panel.grid(row=6, column=1, padx=10, pady=10)
    search_photo(photo_panel, user[3])


    ### Fields ###
    name_field = tkinter.Entry(update_screen)
    name_field.grid(row=0, column=1, padx=10, pady=10)
    name_field.insert(0, user[1])

    validation = (update_screen.register(check_cpf), '%S', '%P')
    cpf_field = tkinter.Entry(update_screen, validate='key', validatecommand=validation)
    cpf_field.grid(row=1, column=1, padx=10, pady=10)
    cpf_field.insert(0, user[0])

    password_field = tkinter.Entry(update_screen, show="*")
    password_field.grid(row=2, column=1, padx=10, pady=10)
    password_field.insert(0, user[2])


    ### Buttons ###
    cancel_button = tkinter.Button(update_screen, text="Cancelar", command=cancel)
    cancel_button.grid(row=3, column=0, padx=10, pady=10)

    change_button = tkinter.Button(update_screen, text="Alterar", command=update)
    change_button.grid(row=3, column=1, padx=10, pady=10)

    photo_button = tkinter.Button(update_screen, text="Escolher foto", command=lambda: search_photo(photo_panel, None, path))
    photo_button.grid(row=6, column=0, padx=10, pady=10)

    update_screen.mainloop()

def delete_user(screen, cpf):
    choice = message.askyesno("Confirmar", "Tem certeza que deseja deletar seu perfil?")

    if choice:
        screen.destroy()
        db.delete_user(connection, cpf)
        main()

def assign_path(screen, user):
    screen.destroy()

    path_screen = tkinter.Tk()
    path_screen.title("Novo Trajeto")

    set_geometry(path_screen, 260, 300)

    paths = db.get_not_my_paths(connection, user[0])


    ### Functions ###
    def assign():
        item = select.selection()

        if item:        
            trajeto_id = select.item(item, "values")[0]
            db.assign_path(connection, trajeto_id, user[0])
            path_screen.destroy()
            home(user)

    def create():
        db.new_path(connection, origin_field.get(), destination_field.get(), user[0])
        path_screen.destroy()
        home(user)

    ### Select ###
    select = ttk.Treeview(path_screen, columns=("Trajeto_Id", "Origem", "Destino"), show="headings")
    select.grid(row=0, column=0, padx=20, pady=20)

    select.heading("Trajeto_Id", text="Id")
    select.heading("Origem", text="Origem")
    select.heading("Destino", text="Destino")

    for path in paths:
        select.insert("", "end", values=(path[0], path[1], path[2]))
            

    ### Labels ###
    origin_label = tkinter.Label(path_screen, text="Origem:")
    origin_label.grid(row=2, column=0, padx=10, pady=10)

    destination_label = tkinter.Label(path_screen, text="Destino:")
    destination_label.grid(row=3, column=0, padx=10, pady=10)


    ### Fields ###
    origin_field = tkinter.Entry(path_screen)
    origin_field.grid(row=2, column=1, padx=10, pady=10)

    destination_field = tkinter.Entry(path_screen)
    destination_field.grid(row=3, column=1, padx=10, pady=10)


    ### Buttons ###
    assign_button = tkinter.Button(path_screen, text="Adicionar Trajeto", command=assign)
    assign_button.grid(row=1, column=0, pady=10)

    add_button = tkinter.Button(path_screen, text="Criar Novo Trajeto", command=create)
    add_button.grid(row=4, column=0, padx=10, pady=10)

    path_screen.mainloop()

def change_path(screen, path, user):
    screen.destroy()

    path_screen = tkinter.Tk()
    path_screen.title("Novo Trajeto")

    set_geometry(path_screen, 260, 300)
    

    ### Function ###
    def change(): 
        db.update_path(connection, origin_field.get(), destination_field.get(), path)
        path_screen.destroy()
        home(user)
            

    ### Labels ###
    origin_label = tkinter.Label(path_screen, text="Origem:")
    origin_label.grid(row=2, column=0, padx=10, pady=10)

    destination_label = tkinter.Label(path_screen, text="Destino:")
    destination_label.grid(row=3, column=0, padx=10, pady=10)


    ### Fields ###
    origin_field = tkinter.Entry(path_screen)
    origin_field.grid(row=2, column=1, padx=10, pady=10)

    destination_field = tkinter.Entry(path_screen)
    destination_field.grid(row=3, column=1, padx=10, pady=10)


    ### Buttons ###
    add_button = tkinter.Button(path_screen, text="Alterar Trajeto", command=lambda: change())
    add_button.grid(row=4, column=0, padx=10, pady=10)

    path_screen.mainloop()

def delete_path(screen, user, path):
    choice = message.askyesno("Confirmar", "Tem certeza que deseja deletar este trajeto?")

    if choice:
        db.delete_path(connection, path)
        screen.destroy()
        home(user)

if __name__ == "__main__":
    main()