import os
import tkinter as tk
from tkinter import filedialog
import GetData_bibtext
import GetData_ristext 
import convertToRis

f = open("myfile.ris", "x")

data = [
    "Autores: ", "Editores: ", "Titulo: ", "Libro: ", "Año de publicacion: ", 
    "Mes de publicacion: ", "Dia de publicacion: ", "Editorial: ", "Direccion: ", 
    "Paginas: ", "Abstract: ", "ISBN: ", "Journal: ", "ISSN: ", "Doi: ", "URL: "
]

# Función para leer el documento
def open_file():
    root = tk.Tk()
    root.withdraw()
    
    file_path = filedialog.askopenfilename(
        title="Selecciona el archivo",
        filetypes=[("BibTeX and RIS files", "*.bib;*.ris"), ("All files", "*.*")]
    )
    
    if file_path:
        _, file_extension = os.path.splitext(file_path)

        with open(file_path, "r", encoding="utf-8") as file:
            contenido = file.read()
            
            # Verifica la extensión del archivo y llama a la función correspondiente
            if file_extension.lower() == ".bib":
                datos = GetData_bibtext.extraer_datos_bibtext(contenido)
                ris_converted = convertToRis.convertir_a_ris(datos)
                f.write(ris_converted)
                f.close


            elif file_extension.lower() == ".ris":
                datos = GetData_ristext.extraer_datos_ris(contenido)

            for datatype, databib in zip(data, datos):
                if databib:
                    print(datatype, databib)


if __name__ == "__main__":
    open_file()
