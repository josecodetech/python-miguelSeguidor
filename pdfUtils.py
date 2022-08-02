from asyncio.windows_events import NULL
from email import message
from fileinput import filename
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile
from tkinter import ttk
from screeninfo import get_monitors
import os
from PyPDF2 import PdfReader, PdfWriter
from fpdf import FPDF
from PIL import Image
# probando fork
# https://pyfpdf.readthedocs.io/en/latest/Tutorial/index.html
# https://pypdf2.readthedocs.io/en/latest/
# tinker validation https://www.pythontutorial.net/tkinter/tkinter-validation/
# string methodds https://www.w3schools.com/python/python_ref_string.asp
# tkinter widgets https://www.studytonight.com/tkinter/python-tkinter-widgets

GRIS = "#9b9897"
FUENTE = ("Arial", 12)
FUENTEENTRY = ("Arial", 30)
# for m in get_monitors():
#    print(str(m))
monitor1 = str(get_monitors()[0])
# print(type(monitor1))
anchoMonitor = int(monitor1.split(", ")[2].split("=")[1])
altoMonitor = int(monitor1.split(", ")[3].split("=")[1])
# print(anchoMonitor)
# print(altoMonitor)
anchoVent = "520"
altoVent = "300"
posX = str(anchoMonitor//2-(int(anchoVent)//2))
posY = str(altoMonitor//2-(int(altoVent)//2))
path = ""


def vaciar(event):
    event.widget.delete(0, END)


def esNumero(texto):
    return texto.isdigit()


def rutaFichero(tipo):
    global path

    dirActual = os.getcwd()
    if (tipo == "PDF"):
        tipos = [("Archivos PDF", "*.pdf")]
        path = filedialog.askopenfilename(initialdir=dirActual,
                                          title="Elige el fichero",
                                          filetypes=tipos)
    elif (tipo == "IMAGEN"):
        tipos = [("Imágenes", "*.jpg"), ("Imágenes", "*.png")]
        path = filedialog.askopenfilenames(initialdir=dirActual,
                                           title="Elige el fichero",
                                           filetypes=tipos)
        print(type(path))
        print(path)
    else:
        return NULL
    try:
        if (len(path) != 0):
            if(tipo == "PDF"):
                nombreArchivo = path.split("/")[-1]
                btnAbrir.configure(text="..."+nombreArchivo[-10:])
                reader = PdfReader(path)
                pagFin.set(len(reader.pages))
            elif(tipo == "IMAGEN"):
                nombreArchivo = path[0].split("/")[-1]
                btnAbrirI.configure(text="..."+nombreArchivo[-10:])
    except:
        print("error")

    return path


def extraerPaginas():
    if compruebaPags():
        if path == "":
            messagebox.showwarning(title="Error", message="Tiene que seleccionar "
                                   "un archivo antes de extraer.", icon="warning")
        else:
            reader = PdfReader(path)
            writer = PdfWriter()
            for x in range(pagInicio.get(), pagFin.get()+1):
                writer.add_page(reader.pages[x-1])
            files = [('PDF Files', '*.pdf')]
            destino = filedialog.asksaveasfilename(
                filetypes=files, defaultextension=files)
            if (destino != ""):
                with open(destino, "wb") as fp:
                    writer.write(fp)
                messagebox.showinfo(title="Correcto", message="Se ha creado el "
                                    "nuevo PDF")


def compruebaPags():
    ini = entryPagInicio.get()
    fin = entryPagFin.get()
    if fin < ini:
        messagebox.showwarning(title="Error", message="La página final "
                               "no puede ser menor a la página inicial.")
        return False
    elif (ini == "" or fin == ""):
        messagebox.showwarning(title="Error", message="Alguna página "
                               "está vacía.")
        return False
    else:
        return True


def guardarImagenPDF():
    if path == "":
        messagebox.showwarning(title="Error", message="Tiene que seleccionar "
                               "una imágen antes de convertir a PDF.")
    else:
        pdf = FPDF('P', 'mm', 'A4')
        for x in path:
            pdf.add_page()
            img = Image.open(x)
            width = img.width
            height = img.height
            pdf.image(x, x=0, y=0, w=(width/3))
        destino = filedialog.asksaveasfilename(
            filetypes=[('PDF Files', '*.pdf')],
            defaultextension=('PDF Files', '*.pdf'))
        if (destino != ""):
            pdf.output(destino, 'F')
            messagebox.showinfo(title="Correcto", message="Se ha creado el "
                                "nuevo PDF")


ventana = Tk()

pagInicio = IntVar(ventana, value="1")
pagFin = IntVar(ventana, value="1")

ventana.title('Herramientas útiles')
ventana.geometry(f"{anchoVent}x{altoVent}+{posX}+{posY}")
ventana.config(background=GRIS)

lblPagIni = Label(ventana, text="Pág Inicial", bg=GRIS, padx=10, pady=10,
                  font=FUENTE)
lblPagIni.grid(column=2, row=0)

lblPagFin = Label(ventana, text="Pág Final", bg=GRIS, padx=10, pady=10,
                  font=FUENTE)
lblPagFin.grid(column=3, row=0)

lblExtrPdf = Label(ventana, text="Extraer páginas\n PDF",
                   bg=GRIS, padx=10, pady=10, font=FUENTE)
lblExtrPdf.grid(column=0, row=1)

lblImagen = Label(ventana, text="Pasar imágen a\n PDF",
                  bg=GRIS, padx=10, pady=10, font=FUENTE)
lblImagen.grid(column=0, row=2)

btnAbrir = Button(ventana, text="Seleccionar\n archivo",
                  command=lambda: rutaFichero("PDF"),
                  font=FUENTE, width=10, height=2)
btnAbrir.grid(column=1, row=1)

'''lblImagenI = Label(ventana,text="Imágen :",
                   bg=GRIS,padx=10,pady=10,font=FUENTE)
lblImagenI.grid(column=1,row=2)'''

btnAbrirI = Button(ventana, text="Seleccionar\n imágen",
                   command=lambda: rutaFichero("IMAGEN"),
                   font=FUENTE, width=10, height=2)
btnAbrirI.grid(column=1, row=2)

btnGuardarI = Button(ventana, text="Convertir a\nPDF",
                     command=guardarImagenPDF,
                     font=FUENTE, width=10, height=2)
btnGuardarI.grid(column=2, row=2, padx=10)

entryPagInicio = Entry(ventana,
                       textvariable=pagInicio,
                       background="white",
                       width=3,
                       validate="key",
                       justify="center",
                       font=FUENTEENTRY,
                       validatecommand=(ventana.register(esNumero), "%S"))

entryPagInicio.grid(column=2, row=1)
'''ipady=16
entryPagInicio.bind("<FocusIn>", vaciar(entryPagInicio))
entryPagInicio = Entry(ventana,textvariable=pagInicio)
entryPagInicio.grid(column=2,row=1)'''
entryPagInicio.bind("<Button-1>", vaciar, "asdf")
entryPagFin = Entry(ventana,
                    textvariable=pagFin,
                    background="white",
                    width=3,
                    validate="key",
                    justify="center",
                    font=FUENTEENTRY,
                    validatecommand=(ventana.register(esNumero), "%S"))

entryPagFin.grid(column=3, row=1)
entryPagFin.bind("<Button-1>", vaciar, "asdf")

btnExtraer = Button(ventana, text="Extraer", command=extraerPaginas,
                    font=FUENTE, height=2)
btnExtraer.grid(column=4, row=1)

btnSalir = Button(ventana, text="Salir", command=exit)
btnSalir.grid(column=1, row=3)

ventana.mainloop()
