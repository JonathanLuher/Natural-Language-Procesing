import re
from spacy.lang.es.stop_words import STOP_WORDS

def normalizar(texto, nlp):
    # Eliminar emoticonos y caracteres especiales
    texto = re.sub(r'[^\w\sáéíóúñ]', ' ', texto)
    
    # Normalización de espacios
    texto = ' '.join(texto.split())
    
    # Procesamiento con spaCy
    doc = nlp(texto.lower())
    
    # Filtrado personalizado
    tokens = []
    for token in doc:
        if not token.is_punct and not token.is_space:
            # Mantener solo sustantivos, adjetivos y verbos
            if token.pos_ in ['NOUN', 'VERB', 'ADJ']:
                # Lematización condicional
                if token.lemma_ not in STOP_WORDS and len(token.lemma_) > 2:
                    tokens.append(token.lemma_)
    
    return ' '.join(tokens)