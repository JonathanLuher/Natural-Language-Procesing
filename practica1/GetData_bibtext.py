import re

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
    bibtex_autores = extraer_nombres(r'author\s*=\s*[{]([\s\S]*?)[}](?=,|\n)', contenido)
    bibtex_editores = extraer_nombres(r'editor\s*=\s*[{]([\s\S]*?)\s*}(?=,|\n)', contenido)

    bibtex_titles = re.findall(r'(?<!book)title\s*=\s*[{]([\s\S]*?)[}]', contenido, re.IGNORECASE)
    titles = [re.sub(r'\n+', ' ', title).strip().replace('\xa0', ' ') for title in bibtex_titles]

    bibtex_booktitle = re.findall(r'booktitle\s*=\s*[{]([\s\S]*?)[}]',contenido, re.IGNORECASE)
    bibtex_año = re.findall(r'year\s*=\s*[{]([\s\S]*?)[}]',contenido, re.IGNORECASE)
    bibtext_month = re.findall(r'month\s*=\s*[{]([\s\S]*?)[}]',contenido, re.IGNORECASE)
    bibtext_day = re.findall(r'day\s*=\s*[{]([\s\S]*?)[}]',contenido, re.IGNORECASE)
    bibtex_publisher = re.findall(r'publisher\s*=\s*[{]([\s\S]*?)[}]',contenido, re.IGNORECASE)
    bibtex_address = re.findall(r'address\s*=\s*[{]([\s\S]*?)[}]',contenido, re.IGNORECASE)
    bibtext_pages = re.findall(r'pages\s*=\s*[{]([\s\S]*?)[}]',contenido, re.IGNORECASE)
    bibtext_abstract = re.findall(r'abstract\s*=\s*[{]([\s\S]*?)[}]',contenido,re.IGNORECASE)
    bibtext_isbn = re.findall(r'isbn\s*=\s*[{]([\s\S]*?)[}]',contenido,re.IGNORECASE)

    bibtex_journal = re.findall(r'journal\s*=\s*[{]([\s\S]*?)[}]',contenido,re.IGNORECASE)
    bibtext_issn = re.findall(r'issn\s*=\s*[{]([\s\S]*?)[}]',contenido, re.IGNORECASE)
    bibtext_doi = re.findall(r'doi\s*=\s*[{]([\s\S]*?)[}]',contenido,re.IGNORECASE)
    bibtext_url = re.findall(r'url\s*=\s*[{]([\s\S]*?)[}]',contenido, re.IGNORECASE)




    datos=[bibtex_autores,bibtex_editores,titles,bibtex_booktitle,bibtex_año,bibtext_month,bibtext_day,bibtex_publisher,bibtex_address,bibtext_pages,bibtext_abstract,bibtext_isbn,bibtex_journal,bibtext_issn,bibtext_doi,bibtext_url]
    return datos