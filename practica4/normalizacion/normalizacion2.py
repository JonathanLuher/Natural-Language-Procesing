import re
from spacy.lang.es.stop_words import STOP_WORDS

def normalizar(texto, nlp):
    # Eliminar URLs y menciones
    texto = re.sub(r'http\S+|@\S+', '', texto)
    
    # Limpieza de caracteres especiales
    texto = re.sub(r'[^\w\sáéíóúñ]', '', texto.lower())
    
    # Tokenización
    doc = nlp(texto)
    
    # Lematización y filtrado
    tokens = [
        token.lemma_ 
        for token in doc 
        if not token.is_stop and 
           not token.is_punct and 
           not token.is_space and 
           len(token.text) > 2
    ]
    
    return ' '.join(tokens)