import re
import json

def cargar_patrones_json():
    with open("patrones_bibtex.json", "r", encoding="utf-8") as json_file:
        return json.load(json_file)

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

#Funcion para extraer nombres
def extraer_nombres(expresion, contenido):
    resultados = re.findall(expresion, contenido, re.IGNORECASE)
    return [procesar_nombres(resultado) for resultado in resultados]

#Funcion que busca la lista de autores y editores
def extraer_datos_bibtext(contenido):
    patrones_bibtex = cargar_patrones_json()  # Cargar los patrones desde el archivo JSON

    bibtex_autores = extraer_nombres(patrones_bibtex['Autores'], contenido)
    bibtex_editores = extraer_nombres(patrones_bibtex['Editores'], contenido)

    bibtex_titles = re.findall(patrones_bibtex['Titulo'], contenido, re.IGNORECASE)
    titles = [re.sub(r'\n+', ' ', title).strip().replace('\xa0', ' ') for title in bibtex_titles]

    bibtex_booktitle = re.findall(patrones_bibtex['Libro'], contenido, re.IGNORECASE)
    bibtex_año = re.findall(patrones_bibtex['Año de publicacion'], contenido, re.IGNORECASE)
    bibtext_month = re.findall(patrones_bibtex['Mes de publicacion'], contenido, re.IGNORECASE)
    bibtext_day = re.findall(patrones_bibtex['Dia de publicacion'], contenido, re.IGNORECASE)
    bibtex_publisher = re.findall(patrones_bibtex['Editorial'], contenido, re.IGNORECASE)
    bibtex_address = re.findall(patrones_bibtex['Direccion'], contenido, re.IGNORECASE)
    bibtext_pages = re.findall(patrones_bibtex['Paginas'], contenido, re.IGNORECASE)
    bibtext_abstract = re.findall(patrones_bibtex['Abstract'], contenido, re.IGNORECASE)
    bibtext_isbn = re.findall(patrones_bibtex['ISBN'], contenido, re.IGNORECASE)

    bibtex_journal = re.findall(patrones_bibtex['Journal'], contenido, re.IGNORECASE)
    bibtext_issn = re.findall(patrones_bibtex['ISSN'], contenido, re.IGNORECASE)
    bibtext_doi = re.findall(patrones_bibtex['DOI'], contenido, re.IGNORECASE)
    bibtext_url = re.findall(patrones_bibtex['URL'], contenido, re.IGNORECASE)
    
    datos=[bibtex_autores,bibtex_editores,titles,bibtex_booktitle,bibtex_año,bibtext_month,bibtext_day,bibtex_publisher,bibtex_address,bibtext_pages,bibtext_abstract,bibtext_isbn,bibtex_journal,bibtext_issn,bibtext_doi,bibtext_url]
    return datos

