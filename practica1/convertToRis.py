
def convertir_a_ris(datos_bibtex):
    ris_referencia = []
    
    #Obtenemos los datos del bibtext
    ris_referencia.append("TY  - JOUR") 
    if datos_bibtex[0]:
        for autor in datos_bibtex[0]:
            ris_referencia.append(f"AU  - {autor}")
    if datos_bibtex[1]:
        for editor in datos_bibtex[1]:
            ris_referencia.append(f"ED  - {editor}")
    if datos_bibtex[2]:
        for title in datos_bibtex[2]:
            ris_referencia.append(f"TI  - {title}")
    if datos_bibtex[3]:
        for booktitle in datos_bibtex[3]:
            ris_referencia.append(f"BT  - {booktitle}")
    if datos_bibtex[4]:
        for año in datos_bibtex[4]:
            ris_referencia.append(f"PY  - {año}")
    if datos_bibtex[5]:
        for mes in datos_bibtex[5]:
            ris_referencia.append(f"IS  - {mes}")
    if datos_bibtex[6]:
        for dia in datos_bibtex[6]:
            ris_referencia.append(f"DA  - {dia}")
    if datos_bibtex[7]:
        for publisher in datos_bibtex[7]:
            ris_referencia.append(f"PB  - {publisher}")
    if datos_bibtex[8]:
        for address in datos_bibtex[8]:
            ris_referencia.append(f"AD  - {address}")
    if datos_bibtex[9]:
        for pages in datos_bibtex[9]:
            ris_referencia.append(f"SP  - {pages}")
    if datos_bibtex[10]:
        for abstract in datos_bibtex[10]:
            ris_referencia.append(f"AB  - {abstract}")
    if datos_bibtex[11]:
        for isbn in datos_bibtex[11]:
            ris_referencia.append(f"SN  - {isbn}")
    if datos_bibtex[12]:
        for journal in datos_bibtex[12]:
            ris_referencia.append(f"JO  - {journal}")
    if datos_bibtex[13]:
        for issn in datos_bibtex[13]:
            ris_referencia.append(f"IS  - {issn}")
    if datos_bibtex[14]:
        for doi in datos_bibtex[14]:
            ris_referencia.append(f"DO  - {doi}")
    if datos_bibtex[15]:
        for url in datos_bibtex[15]:
            ris_referencia.append(f"UR  - {url}")
    ris_referencia.append("ER  -  ")

    # Unir todos los elementos en un string, separándolos por saltos de línea
    return "\n".join(ris_referencia)