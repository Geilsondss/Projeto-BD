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
    path.set("./Projeto-BD/default.jpg")

    photo = Photo.open("./Projeto-BD/default.jpg")
    photo = photo.resize((100, 100))

    photo = PhotoTk.PhotoImage(photo)

    photo_panel.config(image=photo)
    photo_panel.image = photo

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

def home(user):
    home_screen = tkinter.Tk()
    home_screen.title("Menu")

    set_geometry(home_screen, 720, 530)

    my_paths = db.get_paths(connection, user[0], True)


    ### Functions ###
    def leave():
        home_screen.destroy()
        main()


    ### Frames ###
    user_frame = tkinter.Frame(home_screen)
    user_frame.grid(row=0, column=0, padx=20, pady=20)
    
    path_frame = tkinter.Frame(home_screen)
    path_frame.grid(row=1, column=0, padx=20, pady=20, sticky="w")
    
    scroll_frame = tkinter.Frame(home_screen)
    scroll_frame.grid(row=2, column=0, columnspan=30, padx=10, pady=10, sticky="w")
    

    ### Labels ###
    welcome_label = tkinter.Label(user_frame, text="Olá, " + user[1] + "!")
    welcome_label.grid(row=0, column=1, padx=20, sticky="w")

    paths_label = tkinter.Label(path_frame, text="Seus trajetos:")
    paths_label.grid(row=0, column=0, sticky="w")


    ### Panels ###
    photo_panel = tkinter.Label(user_frame)
    photo_panel.grid(row=0, column=0, padx=(0, 10), sticky="w")
    search_photo(photo_panel, user[3])


    ### Buttons ###
    change_button = tkinter.Button(user_frame, text="Alterar", width=10, command=lambda: update_user(home_screen, user))
    change_button.grid(row=0, column=2, padx=10, sticky="w")

    delete_button = tkinter.Button(user_frame, text="Excluir", width=10, command=lambda: delete_user(home_screen, user[0]))
    delete_button.grid(row=0, column=3, padx=10, sticky="w")

    leave_button = tkinter.Button(user_frame, text="Sair", width=10, command=leave)
    leave_button.grid(row=0, column=4, padx=10, sticky="w")

    routes_button = tkinter.Button(scroll_frame, text="Gerenciar Linhas", width=15, command=lambda: manage_routes(home_screen, user))
    routes_button.grid(row=0, column=2, padx=30, pady=10)

    paths_button = tkinter.Button(path_frame, text="Adicionar", width=10, command=lambda: assign_path(home_screen, user))
    paths_button.grid(row=0, column=1, padx=20, pady=10, sticky="w")


    ### Scroll Frame ###
    canvas = tkinter.Canvas(scroll_frame, width=500)
    canvas.grid(row=0, column=0, sticky="nsew")

    scroll = tkinter.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
    scroll.grid(row=0, column=1, sticky="ns")

    canvas.config(yscrollcommand=scroll.set)

    path_frame = tkinter.Frame(canvas)
    canvas.create_window((0, 0), window=path_frame, anchor="nw")

    for i, path in enumerate(my_paths):
        path_label = tkinter.Label(path_frame, text=f"{path[1]} - {path[3]}")
        path_label.grid(row=i, column=2, padx=10, pady=5, sticky="w")

        path_change_button = tkinter.Button(path_frame, text="Alterar", width=6, command=lambda: update_path(home_screen, user, path))
        path_change_button.grid(row=i, column=0, padx=10, pady=5, sticky="w")

        path_delete_button = tkinter.Button(path_frame, text="Excluir", width=6, command=lambda: delete_path(home_screen, user, path))
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
        default_photo(photo_panel, path)
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
    path_screen.title("Trajetos")

    set_geometry(path_screen, 780, 420)
        
    not_my_paths = db.get_paths(connection, user[0], False)
    stations = db.get_stations(connection)

    collect_id = {(path[1], path[3]) : path for path in not_my_paths}
    collect_stations = {station[2] : station[0] for station in stations}

    ### Frames ###
    select_frame = tkinter.Frame(path_screen)
    select_frame.grid(row=0, column=0, columnspan=20, padx=20, pady=(20, 0), sticky="w")
    new_path_frame = tkinter.Frame(path_screen)
    new_path_frame.grid(row=1, column=0, columnspan=20, padx=20, pady=20, sticky="w")


    ### Functions ###
    def assign():
        item = select.selection()

        if item:        
            origin = select.item(item, "values")[0]
            destination = select.item(item, "values")[1]

            path = collect_id[(origin, destination)]

            db.assign_path(connection, path[0], path[2], user[0])

            path_screen.destroy()
            home(user)

    def create():
        origin_name = origin_var.get()
        destination_name = destination_var.get()  

        if origin_name != destination_name:
            origin_id = collect_stations[origin_name]
            destination_id = collect_stations[destination_name]

            if db.new_path(connection, origin_id, destination_id):
                db.assign_path(connection, origin_id, destination_id, user[0])
                path_screen.destroy()
                home(user)
            else:
                message.showinfo("Erro", "Este trajeto já existe, selecione-o")
        else:
            message.showinfo("Erro", "Origem e Destino devem ser diferentes")

    def back():
        path_screen.destroy()
        home(user)


    ### Select ###
    select = ttk.Treeview(select_frame, columns=("Origem", "Destino"), show="headings")
    select.grid(row=0, column=0, sticky="w")

    select.heading("Origem", text="Origem")
    select.heading("Destino", text="Destino")

    select.column("#1", width=300)
    select.column("#2", width=300)

    for path in not_my_paths:
        select.insert("", "end", values=(path[1], path[3]))
            

    ### Labels ###
    origin_label = tkinter.Label(new_path_frame, text="Origem:")
    origin_label.grid(row=0, column=0, pady=10, sticky="w")

    destination_label = tkinter.Label(new_path_frame, text="Destino:")
    destination_label.grid(row=1, column=0, pady=10, sticky="w")


    ### Options ###
    station_option = [station[2] for station in stations]

    origin_var = tkinter.StringVar()
    destination_var = tkinter.StringVar()

    if len(station_option) > 0:
        origin_var.set(station_option[0])
        destination_var.set(station_option[1])

        corp_menu = tkinter.OptionMenu(new_path_frame, origin_var, *station_option)
        corp_menu.grid(row=0, column=1, pady=10, sticky="w")
        path_menu = tkinter.OptionMenu(new_path_frame, destination_var, *station_option)
        path_menu.grid(row=1, column=1, pady=10, sticky="w")
    else:
        origin_var.set("")
        destination_var.set("")

        corp_menu = tkinter.OptionMenu(new_path_frame, origin_var, "")
        corp_menu.grid(row=0, column=1, pady=10, sticky="w")
        path_menu = tkinter.OptionMenu(new_path_frame, destination_var, "")
        path_menu.grid(row=1, column=1, pady=10, sticky="w")


    ### Buttons ###
    assign_button = tkinter.Button(select_frame, text="Adicionar Trajeto", command=assign)
    assign_button.grid(row=0, column=1, padx=28, pady=10, sticky="w")

    add_button = tkinter.Button(new_path_frame, text="Criar Novo Trajeto", command=create)
    add_button.grid(row=2, column=0, pady=10, sticky="w")

    back_button = tkinter.Button(new_path_frame, text="Voltar", width=8, command=back)
    back_button.grid(row=2, column=1, padx=25, pady=10, sticky="w")

    path_screen.mainloop()

def update_path(screen, user, path):
    screen.destroy()

    path_screen = tkinter.Tk()
    path_screen.title("Alterar Trajeto")

    set_geometry(path_screen, 340, 150)

    stations = db.get_stations(connection)

    collect_stations = {station[2] : station[0] for station in stations}
    

    ### Function ###
    def change(): 
        origin_name = origin_var.get()
        destination_name = destination_var.get()  

        if origin_name != destination_name:
            origin_id = collect_stations[origin_name]
            destination_id = collect_stations[destination_name]

            db.update_path(connection, path[0], path[2], user[0], origin_id, destination_id)

            path_screen.destroy()
            home(user)
        else:
            message.showinfo("Erro", "Origem e Destino devem ser diferentes")

    def back():
        path_screen.destroy()
        home(user)


    ### Options ###
    station_option = [station[2] for station in stations]

    origin_var = tkinter.StringVar()
    destination_var = tkinter.StringVar()

    if len(station_option) > 0:
        origin_var.set(path[1])
        destination_var.set(path[3])

        corp_menu = tkinter.OptionMenu(path_screen, origin_var, *station_option)
        corp_menu.grid(row=2, column=1, pady=10, sticky="w")
        path_menu = tkinter.OptionMenu(path_screen, destination_var, *station_option)
        path_menu.grid(row=3, column=1, pady=10, sticky="w")
    else:
        origin_var.set("")
        destination_var.set("")

        corp_menu = tkinter.OptionMenu(path_screen, origin_var, "")
        corp_menu.grid(row=2, column=1, pady=10, sticky="w")
        path_menu = tkinter.OptionMenu(path_screen, destination_var, "")
        path_menu.grid(row=3, column=1, pady=10, sticky="w")
            

    ### Labels ###
    origin_label = tkinter.Label(path_screen, text="Origem:")
    origin_label.grid(row=2, column=0, padx=15, pady=10, sticky="w")

    destination_label = tkinter.Label(path_screen, text="Destino:")
    destination_label.grid(row=3, column=0, padx=15, pady=10, sticky="w")


    ### Buttons ###
    update_button = tkinter.Button(path_screen, text="Alterar Trajeto", command=change)
    update_button.grid(row=4, column=0, padx=(15, 25), pady=10, sticky="w")

    back_button = tkinter.Button(path_screen, text="Voltar", width=8, command=back)
    back_button.grid(row=4, column=1, padx=(0, 0), pady=10, sticky="w")

    path_screen.mainloop()

def delete_path(screen, user, path):
    choice = message.askyesno("Confirmar", "Tem certeza que deseja deletar este trajeto?")

    if choice:
        db.delete_path(connection, user[0], path[0], path[2])
        screen.destroy()
        home(user)

def manage_routes(screen, user):
    screen.destroy()

    manage_screen = tkinter.Tk()
    manage_screen.title("Linhas")

    set_geometry(manage_screen, 880, 515)

    items = db.get_routes(connection)

    collect_items = {item[1] : item for item in items}
    collect_stations = {station[2] : station[0] for station in db.get_stations(connection)}
    collect_corps = {corp[1] : corp[0] for corp in db.get_corps(connection)}
    collect_routes = {item[1] : item[0] for item in items}


    ### Frames ###
    select_frame = tkinter.Frame(manage_screen)
    select_frame.grid(row=0, column=1, columnspan=20, padx=20, sticky="w")
    new_route_frame = tkinter.Frame(manage_screen)
    new_route_frame.grid(row=1, column=0, columnspan=20, padx=20, sticky="w")


    ### Functions ###
    def create():
        if not name_field.get() == "" and not corp_var.get() == "" and not origin_var.get() == "" and not destination_var.get() == "":
            route_name = name_field.get()
            corp_name = corp_var.get()
            origin_name = origin_var.get()  
            destination_name = destination_var.get()

            if not origin_name == destination_name:
                corp_id = collect_corps[corp_name]
                origin_id = collect_stations[origin_name]
                destination_id = collect_stations[destination_name]

                result = db.new_route(connection, route_name, corp_id, origin_id, destination_id)

                if result:
                    manage_routes(manage_screen, user)
                else:
                    message.showerror("Erro", "Já existe uma linha com esse nome")
            else:
                message.showerror("Erro", "Origem e Destino devem ser diferentes")
        else:
            message.showerror("Erro", "Preencha todos os campos")
    
    def update():
        item = select.selection()

        if item:        
            route_name = select.item(item, "values")[0]
            route = collect_items[route_name]

            update_route(manage_screen, user, route, items)

    def delete():
        item = select.selection()

        if item:        
            choice = message.askyesno("Confirmar", "Tem certeza que deseja deletar essa linha?")

            if choice:  
                route_name = select.item(item, "values")[0]
                route_id = collect_routes[route_name]

                db.delete_route(connection, route_id)
                manage_routes(manage_screen, user)  

    def back():
        manage_screen.destroy()
        home(user)


    ### Select ###
    select = ttk.Treeview(manage_screen, columns=("Linha", "Empresa", "Trajeto"), show="headings")
    select.grid(row=0, column=0, padx=(20, 0), pady=20, sticky="w")

    select.heading("Linha", text="Linha")
    select.heading("Empresa", text="Empresa")
    select.heading("Trajeto", text="Trajeto")

    select.column("#1", width=150)
    select.column("#2", width=180)
    select.column("#3", width=340)

    for item in items:
        select.insert("", "end", values=(item[1], item[3], f"{item[5]} - {item[7]}"))


    ### Options ###
    corp_option = [corp[1] for corp in db.get_corps(connection)]
    station_option = [station[2] for station in db.get_stations(connection)]

    corp_var = tkinter.StringVar()
    origin_var = tkinter.StringVar()
    destination_var = tkinter.StringVar()

    if len(corp_option) > 0:
        corp_var.set(corp_option[0])

        corp_menu = tkinter.OptionMenu(new_route_frame, corp_var, *corp_option)
        corp_menu.grid(row=1, column=1, pady=10, sticky="w")
    else:
        corp_var.set("")

        corp_menu = tkinter.OptionMenu(new_route_frame, corp_var, "")
        corp_menu.grid(row=1, column=1, pady=10, sticky="w")

    if len(station_option) > 1:
        origin_var.set(station_option[0])
        destination_var.set(station_option[1])

        origin_menu = tkinter.OptionMenu(new_route_frame, origin_var, *station_option)
        origin_menu.grid(row=2, column=1, pady=10, sticky="w")
        destination_menu = tkinter.OptionMenu(new_route_frame, destination_var, *station_option)
        destination_menu.grid(row=3, column=1, pady=10, sticky="w")
    elif len(station_option) > 0:
        origin_var.set(station_option[0])
        destination_var.set(station_option[0])

        origin_menu = tkinter.OptionMenu(new_route_frame, origin_var, *station_option)
        origin_menu.grid(row=2, column=1, pady=10, sticky="w")
        destination_menu = tkinter.OptionMenu(new_route_frame, destination_var, *station_option)
        destination_menu.grid(row=3, column=1, pady=10, sticky="w")
    else:
        origin_var.set("")
        destination_var.set("")

        origin_menu = tkinter.OptionMenu(new_route_frame, origin_var, "")
        origin_menu.grid(row=2, column=1, pady=10, sticky="w")
        destination_menu = tkinter.OptionMenu(new_route_frame, destination_var, "")
        destination_menu.grid(row=3, column=1, pady=10, sticky="w")
    

    ### Labels ###
    name_label = tkinter.Label(new_route_frame, text="Nome:")
    name_label.grid(row=0, column=0, pady=10, sticky="w")

    corp_label = tkinter.Label(new_route_frame, text="Empresa:")
    corp_label.grid(row=1, column=0, pady=10, sticky="w")

    origin_label = tkinter.Label(new_route_frame, text="Origem:")
    origin_label.grid(row=2, column=0, pady=10, sticky="w")

    destination_label = tkinter.Label(new_route_frame, text="Destino:")
    destination_label.grid(row=3, column=0, pady=10, sticky="w")


    ### Fields ###
    name_field = tkinter.Entry(new_route_frame, width=55)
    name_field.grid(row=0, column=1, pady=10, sticky="w")


    ### Buttons ###
    update_button = tkinter.Button(select_frame, text="Atualizar Linha", width=13, command=update)
    update_button.grid(row=0, column=0, padx=20, pady=10, sticky="w")

    delete_button = tkinter.Button(select_frame, text="Excluir Linha", width=13, command=delete)
    delete_button.grid(row=1, column=0, padx=20, pady=10, sticky="w")

    add_button = tkinter.Button(new_route_frame, text="Criar Nova Linha", command=create)
    add_button.grid(row=4, column=0, pady=10, sticky="w")

    back_button = tkinter.Button(new_route_frame, text="Voltar", width=8, command=back)
    back_button.grid(row=4, column=1, padx=30, pady=10, sticky="w")

    manage_screen.mainloop()

def update_route(screen, user, route, items):
    screen.destroy()

    update_screen = tkinter.Tk()
    update_screen.title("Atualizar Linha")

    set_geometry(update_screen, 433, 252)

    items = db.get_routes(connection)

    collect_stations = {item[5] : item[4] for item in items}
    collect_stations.update({item[7] : item[6] for item in items})
    collect_corps = {item[3] : item[2] for item in items}


    ### Frame ###
    update_route_frame = tkinter.Frame(update_screen)
    update_route_frame.grid(row=0, column=0, padx=(10, 0), sticky="w")
    button_frame = tkinter.Frame(update_screen)
    button_frame.grid(row=1, column=0, padx=(10, 0), pady=10, sticky="w")
    

    ### Functions ###
    def update(): 
        if not name_field.get() == "" and not corp_var.get() == "" and not origin_var.get() == "" and not destination_var.get() == "":
            route_name = name_field.get()
            corp_name = corp_var.get()
            origin_name = origin_var.get()  
            destination_name = destination_var.get()

            if not origin_name == destination_name:
                corp_id = collect_corps[corp_name]
                origin_id = collect_stations[origin_name]
                destination_id = collect_stations[destination_name]

                result = db.update_route(connection, route[0], route[1], route[4], route[6], route_name, corp_id, origin_id, destination_id)

                if result:
                    manage_routes(update_screen, user)
                else:
                    message.showerror("Erro", "Já existe uma linha com esse nome")
            else:
                message.showerror("Erro", "Origem e Destino devem ser diferentes")
        else:
            message.showerror("Erro", "Preencha todos os campos")
    
    def back():
        manage_routes(update_screen, user)
            

    ### Options ###
    corp_option = [corp[1] for corp in db.get_corps(connection)]
    station_option = [station[2] for station in db.get_stations(connection)]

    corp_var = tkinter.StringVar()
    origin_var = tkinter.StringVar()
    destination_var = tkinter.StringVar()

    if len(corp_option) > 0:
        corp_var.set(route[3])

        corp_menu = tkinter.OptionMenu(update_route_frame, corp_var, *corp_option)
        corp_menu.grid(row=1, column=1, pady=10, sticky="w")
    else:
        corp_var.set("")

        corp_menu = tkinter.OptionMenu(update_route_frame, corp_var, "")
        corp_menu.grid(row=1, column=1, pady=10, sticky="w")

    if len(station_option) > 1:
        origin_var.set(route[5])
        destination_var.set(route[7])

        origin_menu = tkinter.OptionMenu(update_route_frame, origin_var, *station_option)
        origin_menu.grid(row=2, column=1, pady=10, sticky="w")
        destination_menu = tkinter.OptionMenu(update_route_frame, destination_var, *station_option)
        destination_menu.grid(row=3, column=1, pady=10, sticky="w")
    elif len(station_option) > 0:
        origin_var.set(route[5])
        destination_var.set(route[5])

        origin_menu = tkinter.OptionMenu(update_route_frame, origin_var, *station_option)
        origin_menu.grid(row=2, column=1, pady=10, sticky="w")
        destination_menu = tkinter.OptionMenu(update_route_frame, destination_var, *station_option)
        destination_menu.grid(row=3, column=1, pady=10, sticky="w")
    else:
        origin_var.set("")
        destination_var.set("")

        origin_menu = tkinter.OptionMenu(update_route_frame, origin_var, "")
        origin_menu.grid(row=2, column=1, pady=10, sticky="w")
        destination_menu = tkinter.OptionMenu(update_route_frame, destination_var, "")
        destination_menu.grid(row=3, column=1, pady=10, sticky="w")


    ### Labels ###
    name_label = tkinter.Label(update_route_frame, text="Nome:")
    name_label.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="w")

    corp_label = tkinter.Label(update_route_frame, text="Empresa:")
    corp_label.grid(row=1, column=0, padx=(0, 10), pady=10, sticky="w")

    origin_label = tkinter.Label(update_route_frame, text="Origem:")
    origin_label.grid(row=2, column=0, padx=(0, 10), pady=10, sticky="w")

    destination_label = tkinter.Label(update_route_frame, text="Destino:")
    destination_label.grid(row=3, column=0, padx=(0, 10), pady=10, sticky="w")


    ### Fields ###
    name_field = tkinter.Entry(update_route_frame, width=55)
    name_field.grid(row=0, column=1, pady=10, sticky="w")
    name_field.insert(0, route[1])


    ### Buttons ###
    update_button = tkinter.Button(button_frame, text="Atualizar Linha", width=13, command=update)
    update_button.grid(row=0, column=0, padx=(0, 20), pady=10, sticky="w")

    back_button = tkinter.Button(button_frame, text="Voltar", width=8, command=back)
    back_button.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="w")

    update_screen.mainloop()

if __name__ == "__main__":
    main()
    #home(['02097726119', 'Victor', 'Leo1', None])