import re

def extraer_datos_ris(contenido):
    patrones = {
        "Autores": r"AU\s*-\s*(.+)",
        "Editores": r"ED\s*-\s*(.+)",
        "Titulo": r"TI\s*-\s*(.+)",
        "Libro": r"BT\s*-\s*(.+)",
        "Año de publicacion": r"PY\s*-\s*(\d+)",
        "Mes de publicacion": r"DA\s*-\s*\d{4}/(\d{2})?",
        "Dia de publicacion": r"DA\s*-\s*\d{4}/\d{2}/(\d{2})?",
        "Editorial": r"PB\s*-\s*(.+)",
        "Direccion": r"CY\s*-\s*(.+)",
        "Paginas": r"SP\s*-\s*(\d+).*?EP  - (\d+)",
        "Abstract": r"AB\s*-\s*(.+)",
        "ISBN": r"SN\s*-\s*([\d-]+)",
        "Journal": r"JO\s*-\s*(.+)",
        "ISSN": r"SN\s*-\s*([\d-]+)",
        "Doi": r"ID\s*-\s*(.+)",
        "URL": r"UR\s*-\s*(.+)"
    }

    datos_extraidos = {}

    for campo, patron in patrones.items():
        coincidencias = re.findall(patron, contenido, re.MULTILINE)
        if coincidencias:
            datos_extraidos[campo] = ", ".join([" ".join(tupla) if isinstance(tupla, tuple) else tupla for tupla in coincidencias])
        else:
            datos_extraidos[campo] = ""

    return [datos_extraidos[campo] for campo in patrones.keys()]
