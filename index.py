from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymongo

MONGO_HOST = "localhost"
MONGO_PORT = "27017"
MONGO_TIMEOUT = 1000

MONGO_URI = "mongodb://"+MONGO_HOST+":"+MONGO_PORT+"/"

MONGO_DB = "escuela"
MONGO_COLECTION = "alumnos"

def showData(table):
    try:
        client = pymongo.MongoClient(
            MONGO_URI, serverSelectionTimeoutMS=MONGO_TIMEOUT)
        client.server_info()
        print("Connected to DB")

        dataBase = client[MONGO_DB]
        colection = dataBase[MONGO_COLECTION]
        for document in colection.find():
            table.insert('',0,text=document["_id"], values=document["nombre"])

        client.close()
    except pymongo.errors.ServerSelectionTimeoutError as timeoutError:
        print("Timeout error "+timeoutError)
    except pymongo.errors.ConnectionFailure as connectionFailure:
        print("Connection failure "+connectionFailure)
    except:
        print("An exception occurred")

def crearRegistro():
    pass

window = Tk()
table = ttk.Treeview(window, columns=2)
table.grid(row=1, column=0)
table.heading("#0",text="ID")
table.heading("#1", text="Nombre")

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

#Boton crear
crear=Button(window, text="Crear alumno", command=crearRegistro, bg="green", fg="white")
crear.grid(row=5, columnspan=2)

showData(table)

window.mainloop()
