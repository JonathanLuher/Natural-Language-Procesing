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

#Funcion que busca la lista de autores
def extraer_autores(contenido):
    return extraer_nombres(r'author\s*=\s*[{"]([\s\S]*?)[}"]', contenido)

def extraer_editores(contenido):
    return extraer_nombres(r'editor\s*=\s*[{"]([\s\S]*?)[}"]', contenido)

#Extraer contenido del titulo
def extraer_titulo(contenido):
    bibtex_titles = re.findall(r'(?<!book)title\s*=\s*[{"]([\s\S]*?)[}"]', contenido, re.IGNORECASE)
    titles = [re.sub(r'\n+', ' ', title).strip().replace('\xa0', ' ') for title in bibtex_titles]
    return titles


#Función para leer el documento

def open_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Selecciona el archivo", filetypes=[("BibTeX and RIS files", "*.bib;*.ris"), ("All files", "*.*")])
    
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            contenido = file.read()

            title = extraer_titulo(contenido)
            authors = extraer_autores(contenido)
            editors = extraer_editores(contenido)
            
            print("Titulo del articulo:", title)
            print("Lista de autores:", authors)
            print("Lista de editores:", editors)
            

if __name__ == "__main__":
    open_file()
