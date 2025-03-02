import tkinter as tk
from tkinter import filedialog
import GetData_bibtext

data=["Autores: ","Editores: ", "Titulo: ", "Libro: ", "Año de publicacion: ","Mes de publicacion: ","Dia de publicacion: ","Editorial: ", "Direccion: ","Paginas: ","Abstract: ", "ISBN: ", "Journal: ","ISSN: ", "Doi: ", "url: "]

#Función para leer el documento
def open_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Selecciona el archivo", filetypes=[("BibTeX and RIS files", "*.bib;*.ris"), ("All files", "*.*")])
    
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            contenido = file.read()
            datos = GetData_bibtext.extraer_datos_bibtext(contenido)

            for datatype, databib in  zip(data,datos):
                print(datatype, databib)
            


if __name__ == "__main__":
    open_file()
