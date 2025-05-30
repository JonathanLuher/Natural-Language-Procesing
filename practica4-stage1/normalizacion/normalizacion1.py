import re
from spacy.lang.es.stop_words import STOP_WORDS

def normalizar(texto, nlp):
    # Limpieza básica
    texto = re.sub(r'[^\w\s]', '', texto.lower())
    
    # Tokenización y lematización
    doc = nlp(texto)
    tokens = [token.lemma_ for token in doc if not token.is_punct]
    
    # Eliminar stopwords
    tokens = [token for token in tokens if token not in STOP_WORDS]
    
    # Unir tokens
    return ' '.join(tokens)