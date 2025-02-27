import re
import tkinter as tk
from tkinter import filedialog

def extraer_autores(contenido):
    bibtex_authors = re.findall(r'author\s*=\s*[{"]([\s\S]*?)[}"]', contenido, re.IGNORECASE)
    authors = [re.sub(r'\n+', ' ', author) for author in bibtex_authors]
    # Reordenar los autores y reemplazar 'and' por comas
    formatted_authors = []
    for author in authors:
        author_list = [name.strip() for name in author.split('and')]
        #Función para reordenar los nombres
        reordered_authors = []
        for name in author_list:
            names = name.split(',') 
            if len(names) == 2:
                reordered_authors.append(f"{names[1].strip()} {names[0].strip()}")
            else:
                reordered_authors.append(name)
        formatted_authors.append(", ".join(reordered_authors))
    return formatted_authors


def extraer_titulo(contenido):
    bibtex_titles = re.findall(r'(?<!book)title\s*=\s*[{"]([\s\S]*?)[}"]', contenido, re.IGNORECASE)
    titles = [re.sub(r'\n+', ' ', title).strip().replace('\xa0', ' ') for title in bibtex_titles]
    return titles

def open_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Selecciona el archivo", filetypes=[("BibTeX and RIS files", "*.bib;*.ris"), ("All files", "*.*")])
    
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            contenido = file.read()
            authors = extraer_autores(contenido)
            print(authors)
            title=extraer_titulo(contenido)
            print(title)

if __name__ == "__main__":
    open_file()
