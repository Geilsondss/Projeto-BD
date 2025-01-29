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

def to_blob(path, photo=None):
    if not photo:
        photo = Photo.open(path.get())
        photo = photo.resize((100, 100)) 

        photo_blob = io.BytesIO()
        photo.save(photo_blob, 'PNG')

        return photo_blob.getvalue()
    return photo

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
            path.set(dir)

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

def default_photo(photo_panel, path):
    path.set("default.jpg")

    photo = Photo.open("default.jpg")
    photo = photo.resize((100, 100))

    photo = PhotoTk.PhotoImage(photo)

    photo_panel.config(image=photo)
    photo_panel.image = photo


### Frames ###

def main():
    main_screen = tkinter.Tk()
    main_screen.title("Sistema Metroviário")

    path = tkinter.StringVar() # Path to photo

    set_geometry(main_screen, 300, 300)


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
        default_photo(photo_panel, path)

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
    default_photo(photo_panel, path)


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

    main_screen.grid_columnconfigure(0, weight=1)
    main_screen.grid_columnconfigure(1, weight=1)
    main_screen.grid_columnconfigure(2, weight=1)

    main_screen.grid_rowconfigure(0, weight=1, uniform="equal")

    main_screen.mainloop()

    connection.close()

def home(user):
    home_screen = tkinter.Tk()
    home_screen.title("Menu")

    set_geometry(home_screen, 720, 480)

    paths = db.get_my_paths(connection, user[0])


    ### Functions ###
    def leave():
        home_screen.destroy()
        main()
    

    ### Labels ###
    welcome_label = tkinter.Label(home_screen, text="Olá, " + user[1] + "!")
    welcome_label.grid(row=0, column=1, padx=20, pady=20)

    paths_label = tkinter.Label(home_screen, text="Seus trajetos:")
    paths_label.grid(row=3, column=0, padx=(20, 0), pady=20, sticky="w")


    ### Panels ###
    photo_panel = tkinter.Label(home_screen)
    photo_panel.grid(row=0, column=0, padx=20, pady=10)
    search_photo(photo_panel, user[3])


    ### Buttons ###
    change_button = tkinter.Button(home_screen, text="Alterar", width=10, command=lambda: update_user(home_screen, user))
    change_button.grid(row=0, column=2, padx=10, pady=10)

    delete_button = tkinter.Button(home_screen, text="Excluir", width=10, command=lambda: delete_user(home_screen, user[0]))
    delete_button.grid(row=0, column=3, padx=10, pady=10)

    leave_button = tkinter.Button(home_screen, text="Sair", width=10, command=leave)
    leave_button.grid(row=0, column=4, padx=10, pady=10)

    paths_button = tkinter.Button(home_screen, text="Adicionar", width=10, command=lambda: assign_path(home_screen, user))
    paths_button.grid(row=3, column=1, pady=10, sticky="w")


    ### Scroll Frame ###
    frame = tkinter.Frame(home_screen)
    frame.grid(row=4, column=0, columnspan=10, padx=10, pady=10, sticky="w")

    canvas = tkinter.Canvas(frame)
    canvas.grid(row=0, column=0, sticky="nsew")

    scroll = tkinter.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scroll.grid(row=0, column=1, sticky="ns")

    canvas.config(yscrollcommand=scroll.set)

    path_frame = tkinter.Frame(canvas)
    canvas.create_window((0, 0), window=path_frame, anchor="nw")

    for i, path in enumerate(paths):
        path_label = tkinter.Label(path_frame, text=f"Origem: {path[1]} - Destino: {path[2]}")
        path_label.grid(row=i, column=2, padx=10, pady=5, sticky="w")

        path_change_button = tkinter.Button(path_frame, text="Alterar", width=6, command=lambda: change_path(home_screen, path, user))
        path_change_button.grid(row=i, column=0, padx=10, pady=5, sticky="w")

        path_delete_button = tkinter.Button(path_frame, text="Excluir", width=6, command=lambda: delete_path(home_screen, user, path[0]))
        path_delete_button.grid(row=i, column=1, padx=10, pady=5, sticky="w")

    path_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    home_screen.mainloop()

def update_user(screen, user):
    screen.destroy()

    update_screen = tkinter.Tk()
    update_screen.title("Alterar usuário")

    path = tkinter.StringVar()

    set_geometry(update_screen, 300, 300)


    ### Functions ###
    def update():
        name = name_field.get()
        cpf = cpf_field.get()
        password = password_field.get()
        photo = to_blob(path, user[3])

        if not name or not password or not cpf:
            message.showwarning("Erro", "Preencha todos os campos")
            return
        
        if len(cpf) < 11:
            message.showwarning("Erro", "Preencha um CPF válido")
            return

        message.showinfo("Sucesso", "Usuário atualizado com sucesso")

        new_user = db.update_user(connection, user[0], name_field.get(), cpf_field.get(), password_field.get(), photo)
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
    if user[3] == None:
        default_photo(photo_panel)
    else:
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
    cancel_button = tkinter.Button(update_screen, width=6, text="Voltar", command=cancel)
    cancel_button.grid(row=3, column=0, padx=10, pady=10)

    change_button = tkinter.Button(update_screen, width=6,  text="Alterar", command=update)
    change_button.grid(row=3, column=1, padx=10, pady=10)

    photo_button = tkinter.Button(update_screen, text="Escolher foto", command=lambda: search_photo(photo_panel, None, path))
    photo_button.grid(row=6, column=0, padx=10, pady=10)

    update_screen.grid_columnconfigure(0, weight=1)
    update_screen.grid_columnconfigure(1, weight=1)
    update_screen.grid_columnconfigure(2, weight=1)

    update_screen.grid_rowconfigure(0, weight=1, uniform="equal")

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

    set_geometry(path_screen, 780, 385)

    paths = db.get_not_my_paths(connection, user[0])

    select_frame = tkinter.Frame(path_screen)
    select_frame.grid(row=0, column=0, columnspan=20, padx=20, sticky="w")
    new_path_frame = tkinter.Frame(path_screen)
    new_path_frame.grid(row=1, column=0, columnspan=20, padx=20, pady=20, sticky="w")


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

    def back():
        path_screen.destroy()
        home(user)

    ### Select ###
    select = ttk.Treeview(select_frame, columns=("Trajeto_Id", "Origem", "Destino"), show="headings")
    select.grid(row=0, column=0, sticky="w")

    select.heading("Trajeto_Id", text="Id")
    select.heading("Origem", text="Origem")
    select.heading("Destino", text="Destino")

    for path in paths:
        select.insert("", "end", values=(path[0], path[1], path[2]))
            

    ### Labels ###
    origin_label = tkinter.Label(new_path_frame, text="Origem:")
    origin_label.grid(row=0, column=0, pady=10, sticky="w")

    destination_label = tkinter.Label(new_path_frame, text="Destino:")
    destination_label.grid(row=1, column=0, pady=10, sticky="w")


    ### Fields ###
    origin_field = tkinter.Entry(new_path_frame)
    origin_field.grid(row=0, column=1, pady=10, sticky="w")

    destination_field = tkinter.Entry(new_path_frame)
    destination_field.grid(row=1, column=1, pady=10, sticky="w")


    ### Buttons ###
    assign_button = tkinter.Button(select_frame, text="Adicionar Trajeto", command=assign)
    assign_button.grid(row=0, column=1, padx=40, pady=10, sticky="w")

    add_button = tkinter.Button(new_path_frame, text="Criar Novo Trajeto", command=create)
    add_button.grid(row=2, column=0, pady=10, sticky="w")

    back_button = tkinter.Button(new_path_frame, text="Voltar", command=back)
    back_button.grid(row=2, column=1, padx=25, pady=10, sticky="w")

    path_screen.mainloop()

def change_path(screen, path, user):
    screen.destroy()

    path_screen = tkinter.Tk()
    path_screen.title("Novo Trajeto")

    set_geometry(path_screen, 260, 140)
    

    ### Function ###
    def change(): 
        db.update_path(connection, origin_field.get(), destination_field.get(), path[0])
        path_screen.destroy()
        home(user)

    def back():
        path_screen.destroy()
        home(user)
            

    ### Labels ###
    origin_label = tkinter.Label(path_screen, text="Origem:")
    origin_label.grid(row=2, column=0, padx=25, pady=10, sticky="w")

    destination_label = tkinter.Label(path_screen, text="Destino:")
    destination_label.grid(row=3, column=0, padx=25, pady=10, sticky="w")


    ### Fields ###
    origin_field = tkinter.Entry(path_screen)
    origin_field.grid(row=2, column=1, padx=10, pady=10)
    origin_field.insert(0, path[1])

    destination_field = tkinter.Entry(path_screen)
    destination_field.grid(row=3, column=1, padx=10, pady=10)
    destination_field.insert(0, path[2])


    ### Buttons ###
    back_button = tkinter.Button(path_screen, text="Voltar", command=back)
    back_button.grid(row=4, column=0, padx=25, pady=10, sticky="w")

    add_button = tkinter.Button(path_screen, text="Alterar Trajeto", command=change)
    add_button.grid(row=4, column=1, padx=10, pady=10, sticky="w")

    path_screen.mainloop()

def delete_path(screen, user, path):
    choice = message.askyesno("Confirmar", "Tem certeza que deseja deletar este trajeto?")

    if choice:
        db.delete_path(connection, path)
        screen.destroy()
        home(user)

if __name__ == "__main__":
    main()