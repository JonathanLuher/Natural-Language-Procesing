import re
from spacy.lang.es.stop_words import STOP_WORDS

def normalizar(texto, nlp):
    # Limpieza 
    texto = re.sub(r'\d+', '', texto)  # Eliminar números
    texto = re.sub(r'\s+', ' ', texto)  # Eliminar espacios múltiples
    
    # Tokenización y análisis morfológico
    doc = nlp(texto.lower())
    
    # Filtrado 
    tokens = [
        token.lemma_ 
        for token in doc 
        if not token.is_stop and 
           not token.is_punct and 
           token.pos_ in ['NOUN', 'VERB', 'ADJ'] and 
           len(token.text) > 3
    ]
    
    return ' '.join(tokens)