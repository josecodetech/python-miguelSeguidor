from fileinput import filename
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from screeninfo import get_monitors
import os

#for m in get_monitors():
#    print(str(m))
monitor1 = str(get_monitors()[0])
#print(type(monitor1))
anchoMonitor = int(monitor1.split(", ")[2].split("=")[1])
altoMonitor = int(monitor1.split(", ")[3].split("=")[1])
#print(anchoMonitor)
#print(altoMonitor)
anchoVent = "500"
altoVent = "300"
posX = str(anchoMonitor//2-(int(anchoVent)//2))
posY = str(altoMonitor//2-(int(altoVent)//2))

def vaciar(event):
    #event.delete(0,END)
    #print()
    print(event.widget)
    event.widget.delete(0, END)

def esNumero(texto):
    #print(type(texto))
    return texto.isdigit()

def abrirFicheros():
    dirActual = os.getcwd()
    filename = filedialog.askopenfilename(initialdir=dirActual,
                                          title="Elige el fichero",
                                          filetypes=[("Archivos PDF",
                                                      "*.pdf")])
    print(filename)
    nombreArchivo = filename.split("/")[-1]
    if nombreArchivo != "":
        btnAbrir.configure(text=nombreArchivo)
    print(pagInicio.get())

ventana = Tk()

pagInicio = IntVar(ventana,value="1")

ventana.title('Herramientas útiles')
ventana.geometry(f"{anchoVent}x{altoVent}+{posX}+{posY}")
ventana.config(background="white")

lblPagIni = Label(ventana,text="Pág Inicial",bg="white",padx=10,pady=10)
lblPagIni.grid(column=2,row=0)

lblPagFin = Label(ventana,text="Pág Final",bg="white",padx=10,pady=10)
lblPagFin.grid(column=3,row=0)

lblExtrPdf = Label(ventana,text="Extraer páginas PDF",
                   bg="white",padx=10,pady=10)
lblExtrPdf.grid(column=0,row=1)

btnAbrir = Button(ventana,text="Seleccionar archivo",command=abrirFicheros)
btnAbrir.grid(column=1, row=1)

entryPagInicio = Entry(ventana,
      textvariable=pagInicio,
      bg="white",
      width=8,
      validate="key",
      validatecommand=(ventana.register(esNumero), "%S"))

entryPagInicio.grid(column=2,row=1)

#entryPagInicio.bind("<FocusIn>", vaciar(entryPagInicio))
entryPagInicio.bind("<Button-1>", vaciar,"asdf")
#entryPagInicio = Entry(ventana,textvariable=pagInicio)
#entryPagInicio.grid(column=2,row=1)

btnSalir = Button(ventana,text="Salir",command=exit)


btnSalir.grid(column=1, row=3)

ventana.mainloop()