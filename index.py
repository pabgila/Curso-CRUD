from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymongo
from bson.objectid import ObjectId

MONGO_HOST = "localhost"
MONGO_PORT = "27017"
MONGO_TIMEOUT = 1000

MONGO_URI = "mongodb://"+MONGO_HOST+":"+MONGO_PORT+"/"

MONGO_DB = "escuela"
MONGO_COLECTION = "alumnos"

ID_ALUMNO = ""

BUTTON_STATUS = "Crear" #CREAR o EDITAR

def showData():
    table.delete(*table.get_children()) #clear table
    try:
        for document in colection.find():
            table.insert('',0,text=document["_id"], values=document["nombre"])
    except pymongo.errors.ServerSelectionTimeoutError as timeoutError:
        print("Timeout error "+timeoutError)
    except pymongo.errors.ConnectionFailure as connectionFailure:
        print("Connection failure "+connectionFailure)
    except:
        print("An exception occurred")

def crearRegistro():
    if len(nombre.get())!=0 and len(sexo.get())!=0 and len(calificacion.get())!=0 :
        try:
            documento={"nombre":nombre.get(),"sexo":sexo.get(),"calificacion":calificacion.get()}
            print(documento)
            colection.insert_one(documento)

            #borrar texto del input
            nombre.delete(0,END)
            sexo.delete(0,END)
            calificacion.delete(0,END)
        except pymongo.errors.ConnectionFailure as error:
            print(error)
        showData()
    else:
        messagebox.showerror(message="Rellene todos los campos")

def editarRegistro():
    pass

def buttonClicked():
    if BUTTON_STATUS == "CREAR":
        crearRegistro()
    else:
        editarRegistro()

def dobleClickTabla(evt):
    global ID_ALUMNO
    global BUTTON_STATUS
    ID_ALUMNO = str(table.item(table.selection())["text"])
    BUTTON_STATUS = "Editar"
    button.config(text=BUTTON_STATUS + " alumno")
    
    #Get data from db
    alumno = colection.find({"_id":ObjectId(ID_ALUMNO)})[0]

    nombre.delete(0,END)
    nombre.insert(0,alumno["nombre"])
    sexo.delete(0,END)
    sexo.insert(0,alumno["sexo"])
    calificacion.delete(0,END)
    calificacion.insert(0,alumno["calificacion"])

client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=MONGO_TIMEOUT)
dataBase = client[MONGO_DB]
colection = dataBase[MONGO_COLECTION]

window = Tk()
table = ttk.Treeview(window, columns=2)
table.grid(row=1, column=0, columnspan=2)
table.heading("#0",text="ID")
table.heading("#1", text="Nombre")
table.bind("<Double-Button-1>",dobleClickTabla)

#Name
Label(window,text="Nombre").grid(row=2, column=0)
nombre=Entry(window)
nombre.grid(row=2, column=1) 

#Sexo
Label(window,text="Sexo").grid(row=3, column=0)
sexo=Entry(window)
sexo.grid(row=3, column=1)

#Calificacion
Label(window,text="Calificación").grid(row=4, column=0)
calificacion=Entry(window)
calificacion.grid(row=4, column=1)

#Boton crear/editar
button=Button(window, text=BUTTON_STATUS + " alumno", command=buttonClicked, bg="green", fg="white")
button.grid(row=5, columnspan=2)

showData()

window.mainloop()
client.close()