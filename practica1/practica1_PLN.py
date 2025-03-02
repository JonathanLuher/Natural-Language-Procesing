import tkinter as tk
from tkinter import filedialog
import GetData_bibtext

#Función para leer el documento
def open_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Selecciona el archivo", filetypes=[("BibTeX and RIS files", "*.bib;*.ris"), ("All files", "*.*")])
    
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            contenido = file.read()
            datos = GetData_bibtext.extraer_datos_bibtext(contenido)
            
            print(
            "Autores: ",datos[0],
            "\nEditores: ",datos[1],
            "\nTitulo: ",datos[2],
            "\nLibro: ",datos[3],
            "\nAño de publicacion: ",datos[4],
            "\nEditorial: ",datos[5],
            "\nDireccion: ",datos[6],
            "\nPaginas: ",datos[7],
            "\nAbstract: ",datos[8],
            "\nISBN: ",datos[9]
            )

if __name__ == "__main__":
    open_file()
