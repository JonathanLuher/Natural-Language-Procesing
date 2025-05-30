import re

def normalizar(texto, nlp):
    # Eliminar hashtags y signos de puntuación
    texto = re.sub(r'#\w+', '', texto)
    texto = re.sub(r'[^\w\s]', ' ', texto)
    
    # Convertir a minúsculas
    texto = texto.lower()
    
    # Tokenización sin lematización
    doc = nlp(texto)
    tokens = [token.text for token in doc if not token.is_punct and not token.is_space]
    
    # Eliminar palabras cortas
    tokens = [token for token in tokens if len(token) > 2]
    
    return ' '.join(tokens)