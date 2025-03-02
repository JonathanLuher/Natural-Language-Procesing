import re
import tkinter as tk
from tkinter import filedialog

#funciones para formatear y reordenar listas de nombres
def procesar_nombres(texto):
    texto = re.sub(r'\n+', ' ', texto)
    nombres_lista = [name.strip() for name in texto.split('and')]
    nombres_reordenados = []
    for name in nombres_lista:
        partes = name.split(',')
        if len(partes) == 2:
            nombres_reordenados.append(f"{partes[1].strip()} {partes[0].strip()}")
        else:
            nombres_reordenados.append(name)
    return ", ".join(nombres_reordenados)

def extraer_nombres(expresion, contenido):
    resultados = re.findall(expresion, contenido, re.IGNORECASE)
    return [procesar_nombres(resultado) for resultado in resultados]

#Funcion que busca la lista de autores y editores
def extraer_datos_bibtext(contenido):
    bibtex_autores = extraer_nombres(r'author\s*=\s*[{]([\s\S]*?)[}](?=,|\n)', contenido)
    bibtex_editores = extraer_nombres(r'editor\s*=\s*[{]([\s\S]*?)\s*}(?=,|\n)', contenido)

    bibtex_titles = re.findall(r'(?<!book)title\s*=\s*[{]([\s\S]*?)[}]', contenido, re.IGNORECASE)
    titles = [re.sub(r'\n+', ' ', title).strip().replace('\xa0', ' ') for title in bibtex_titles]

    bibtex_booktitle = re.findall(r'booktitle\s*=\s*[{]([\s\S]*?)[}]',contenido, re.IGNORECASE)
    bibtex_año = re.findall(r'year\s*=\s*[{]([\s\S]*?)[}]',contenido, re.IGNORECASE)
    bibtex_publisher = re.findall(r'publisher\s*=\s*[{]([\s\S]*?)[}]',contenido, re.IGNORECASE)
    bibtex_address = re.findall(r'address\s*=\s*[{]([\s\S]*?)[}]',contenido, re.IGNORECASE)
    bibtext_pages = re.findall(r'pages\s*=\s*[{]([\s\S]*?)[}]',contenido, re.IGNORECASE)
    bibtext_abstract = re.findall(r'abstract\s*=\s*[{]([\s\S]*?)[}]',contenido,re.IGNORECASE)

    datos=[bibtex_autores,bibtex_editores,titles,bibtex_booktitle,bibtex_año,bibtex_publisher,bibtex_address,bibtext_pages,bibtext_abstract]
    return datos

#Función para leer el documento
def open_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Selecciona el archivo", filetypes=[("BibTeX and RIS files", "*.bib;*.ris"), ("All files", "*.*")])
    
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            contenido = file.read()
            datos = extraer_datos_bibtext(contenido)
            
            print(
            "Autores: ",datos[0],
            "\nEditores: ",datos[1],
            "\nTitulo: ",datos[2],
            "\nLibro: ",datos[3],
            "\nAño de publicacion: ",datos[4],
            "\nEditorial: ",datos[5],
            "\nDireccion: ",datos[6],
            "\nPaginas: ",datos[7],
            "\nAbstract: ",datos[8]
            )

if __name__ == "__main__":
    open_file()
