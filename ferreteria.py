from http.client import PRECONDITION_FAILED
from itertools import product
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector



try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mikebd"
    )
except mysql.connector.Error as e:
    messagebox.showerror("Error de conexión",
                         f"No se pudo conectar a la base de datos: {e}")
    exit()




def leer_usuarioDB():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()



ventana = tk.Tk()
ventana.title("ferreteria")
ventana.geometry("280x450+300+250")



logusuario_limit = StringVar()
logcontra_limit = StringVar()

regnombre_limit = StringVar()
regapellido_limit = StringVar()
regusuario_limit = StringVar()
regcontra_limit = StringVar()
regcontrarep_limit = StringVar()




def enterven1(event):
    login_contraseña.focus_set()



Label(ventana, text="Login").pack()

Label(ventana, text="Usuario : ").pack()
login_usuario = Entry(ventana, textvariable=logusuario_limit)
login_usuario.pack()
login_usuario.bind("<Return>", enterven1)

Label(ventana, text="Contraseña : ").pack()
login_contraseña = Entry(ventana, textvariable=logcontra_limit, show="*")
login_contraseña.pack()


logusuario_limit.trace("w", lambda *args: character_limit(logusuario_limit))
logcontra_limit.trace("w", lambda *args: character_limit(logcontra_limit))




def character_limit(x):
    if len(x.get()) > 0:
        x.set(x.get()[:10])




def login():
    usuario = login_usuario.get()
    contr = login_contraseña.get()
    cursor = db.cursor()
    cursor.execute("SELECT contrasenia FROM users WHERE usuario='" +
                   usuario+"' and contrasenia='"+contr+"'")

    if cursor.fetchall():
        abrirMenu()

    else:
        messagebox.showerror(title="Login incorrecto",
                             message="Usuario o contraseña incorrecto")




def VentanaNueva():

    newVentana = tk.Toplevel(ventana)
    newVentana.title("FERRETERIA GARROTE")
    newVentana.geometry("300x290+800+250")



    def registro1(event):
        entrada_apellido.focus_set()
    def registro2(event):
        entrada_usuario.focus_set()
    def registro3(event):
        entrada_contraseña.focus_set()
    def registro4(event):
        repetir_contraseña.focus_set()
    


    labeExample = tk.Label(newVentana, text="Registro : ").pack

    Label(newVentana, text="Nombre : ").pack()
    entrada_nombre = Entry(newVentana, textvariable=regnombre_limit)
    entrada_nombre.pack()
    entrada_nombre.bind("<Return>", registro1)

    Label(newVentana, text="Apellidos : ").pack()
    entrada_apellido = Entry(newVentana, textvariable=regapellido_limit)
    entrada_apellido.pack()
    entrada_apellido.bind("<Return>", registro2)

    Label(newVentana, text="Usuario : ").pack()
    entrada_usuario = Entry(newVentana, textvariable=regusuario_limit)
    entrada_usuario.pack()
    entrada_usuario.bind("<Return>", registro3)

    Label(newVentana, text="Contraseña : ").pack()
    entrada_contraseña = Entry(newVentana, textvariable=regcontra_limit, show="*")
    entrada_contraseña.pack()
    entrada_contraseña.bind("<Return>", registro4)

    Label(newVentana, text="Repita la Contraseña : ").pack()
    repetir_contraseña = Entry(newVentana, textvariable=regcontrarep_limit, show="*")
    repetir_contraseña.pack()

    regnombre_limit.trace("w", lambda *args: character_limit2(regnombre_limit))
    regapellido_limit.trace(
        "w", lambda *args: character_limit2(regapellido_limit))
    regusuario_limit.trace(
        "w", lambda *args: character_limit(regusuario_limit))
    regcontra_limit.trace("w", lambda *args: character_limit(regcontra_limit))
    regcontrarep_limit.trace(
        "w", lambda *args: character_limit(regcontrarep_limit))


    def character_limit2(x):
        if len(x.get()) > 0:
            x.set(x.get()[:16])


    def usuarioDB(nombre, apellido, usuario, contrasenia):
        try:
            cursor = db.cursor()
            cursor.execute("INSERT INTO users (nombre, apellido, usuario, contrasenia) VALUES (%s, %s, %s, %s)",
                           (nombre, apellido, usuario, contrasenia))
            db.commit()

        except mysql.connector.Error as error:
            messagebox.showerror("Error al agregar el usuario",
                                 f"No se pudo agregar el usuario: {error}")
        finally:
            cursor.close



    def agregar_user():

        cursor = db.cursor()

   

        Nombre = entrada_nombre.get()
        Apellido = entrada_apellido.get()
        Usr_reg = entrada_usuario.get()
        Contra_reg = entrada_contraseña.get()
        Contra_reg_2 = repetir_contraseña.get()


        if not Nombre or not Apellido or not Usr_reg or not Contra_reg or not Contra_reg_2:
            messagebox.showerror("Error al agregar el usuario",
                                 "Por favor ingrese todos los datos del usuario")
            return

       

        if (Contra_reg == Contra_reg_2):

            cursor.execute("INSERT INTO users (nombre, apellido, usuario, contrasenia) VALUES (%s, %s, %s, %s)",
                           (Nombre, Apellido, Usr_reg, Contra_reg))
            db.commit()
            messagebox.showinfo(title="Registro Correcto", message="Hola " +
                                Nombre+" "+Apellido+" ¡¡ \nSu registro fue exitoso.")
            newVentana.destroy()
        else:
            messagebox.showerror(title="Contraseña Incorrecta",
                                 message="Error¡¡¡ \nLas contraseñas no coinciden.")
            entrada_contraseña.delete(0, END)
            repetir_contraseña.delete(0, END)



            usuarioDB(Nombre, Apellido, Usr_reg, Contra_reg)

    buttons = tk.Button(newVentana, text="Registrece ¡",
                        command=agregar_user).pack(side="bottom")


Label(ventana, text=" ").pack()
Button(text=" Acceder ", command=login, bg='#a6d4f2').pack()
Label(ventana, text=" ").pack()
Label(ventana, text="¿quieres crear una cuenta? : ").pack()
boton1 = Button(ventana, text="REGISTRO", bg='#a6d4f2',
                command=VentanaNueva).pack()




def valoresDB():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM productos")
    return cursor.fetchall()



def abrirMenu():
    MenuLR = tk.Toplevel(ventana)
    ventana.withdraw()
    MenuLR.title("ferreteria")
    MenuLR.geometry("900x500")


    def menu1(event):
        product.focus_set()
    def menu2(event):
        cantidad_limit.focus_set()
    def menu3(event):
        PRECONDITION_FAILED.focus_set()


    frame1 = Frame(MenuLR)
    frame1.grid(rowspan=2, column=1, row=1)

    producto_limit = StringVar()
    cantidad_limit = StringVar()
    precio_limit = StringVar()


        
    
    def agregar_valoresDB(producto, cantidad, precio,):
        try:
            cursor = db.cursor()
            cursor.execute("INSERT INTO productos (producto,cantidad,precio) VALUES (%s, %s, %s,)",
                            (producto, cantidad, precio))
            db.commit()

        except mysql.connector.Error as error:
            messagebox.showerror("Error al agregar los productos",
                                f"No se pudo agregar los productos: {error}")
        finally:
            cursor.close




    def agregar_valores():
    

        cursor = db.cursor()



        producto =  entrada_producto.get()
        cantidad = entrada_cantidad.get()
        precio = entrada_precio.get()
      



        if not producto or not cantidad or not precio:
            messagebox.showerror("Error al agregar el usuario",
                                 "Por favor llene los campos requeridos")
            return



        agregar_valoresDB(producto, cantidad, precio)

    def mostrar_productos():
        cursor = db.cursor()
        sql = "SELECT * FROM productos " 
        cursor.execute(sql)
        registro = cursor.fetchall()
        for dato in registro:                       
            tabla.insert('',END, text = dato[1], values=(dato[2], dato[3]))
            


    def borrar_valoresDB():
        cursor = db.cursor()
        select_item =tabla.selection()[0]
        linea = tabla.item(select_item)["values"][1]
        cursor.execute("DELETE FROM productos WHERE producto=%s",(linea,))
        tabla.delete(select_item)
        db.commit()
        cursor.close
        


    Label(MenuLR, text="FERRETERIA GARROTE", font=(
        "Rockwell")).place(x=700, y=5)

    Label(MenuLR, text="producto:", font=(
        "Rockwell", 10)).place(x=150, y=20)
    entrada_producto = Entry(MenuLR, textvariable=producto_limit)
    entrada_producto.place(x=120, y=60)
    entrada_producto.bind("<Return>",menu1)

    Label(MenuLR, text="cantidad:", font=(
        "Rockwell", 10)).place(x=280, y=20)
    entrada_cantidad = Entry(MenuLR, textvariable=cantidad_limit)
    entrada_cantidad.place(x=250, y=60)
    entrada_cantidad.bind("<Return>",menu2)

    Label(MenuLR, text="precio:", font=(
        "Rockwell", 10)).place(x=400, y=20)
    entrada_precio = Entry(MenuLR, textvariable=precio_limit)
    entrada_precio.place(x=380, y=60)
    entrada_precio.bind("<Return>", menu3)


    boton_agregar = Button(MenuLR, text="AGREGAR", font=('Times New Roman',10,'bold'),
                command=agregar_valores)
    boton_agregar.place(x=350, y=100)

    boton_mostrar = Button(MenuLR, command = mostrar_productos, text='MOSTRAR DATOS', font=('Times New Roman',10,'bold'))
    boton_mostrar.place(x=450, y=100)

    boton_eliminar = Button(MenuLR, command = borrar_valoresDB, text=' BORRAR ', font=('Times New Roman',10,'bold'))
    boton_eliminar.place(x=600, y=100)



    producto_limit.trace("w", lambda *args: character_limit3(producto_limit))
    cantidad_limit.trace("w", lambda *args: character_limit3(cantidad_limit))
    precio_limit.trace("w", lambda *args: character_limit3(precio_limit))


    def character_limit3(x):
        if len(x.get()) > 0:
            x.set(x.get()[:20])

    def character_limit4(x):
        if len(x.get()) > 0:
            x.set(x.get()[:7])



    tabla = ttk.Treeview(MenuLR, height= 30,  columns=(
        "#1", "#2", "#3" , ), padding=2)
    tabla.place(x=200, y=180, width=600, height=460)

    tabla.heading("#0", text="productos", anchor='center')
    tabla.heading("#1", text="cantidad", anchor='center')
    tabla.heading("#2", text="precio", anchor='center')


    tabla.column("#0", width=150, minwidth=75, anchor='center')
    tabla.column("#1", width=150, minwidth=75, anchor='center')
    tabla.column("#2", width=150, minwidth=75, anchor='center')




ventana.mainloop()