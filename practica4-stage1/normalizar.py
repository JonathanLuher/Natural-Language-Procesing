import os
import pandas as pd
import spacy
from normalizacion import normalizacion1, normalizacion2, normalizacion3, normalizacion4, normalizacion5

# Cargar el modelo de spaCy para español
nlp = spacy.load('es_core_news_sm')

def cargar_datos():
    # Cargar el corpus desde el archivo CSV
    ruta_corpus = os.path.join('corpus', 'TA1C_dataset_detection_train.csv')
    datos = pd.read_csv(ruta_corpus)
    return datos

def aplicar_normalizacion_y_guardar(datos):
    # Crear las carpetas si no existen
    for i in range(1, 6):
        os.makedirs(f'corpus/normalizacion{i}', exist_ok=True)
    
    # Aplicar cada normalización y guardar el corpus resultante
    normalizaciones = [
        (normalizacion1, 1),
        (normalizacion2, 2),
        (normalizacion3, 3),
        (normalizacion4, 4),
        (normalizacion5, 5)
    ]
    
    for norm_func, num in normalizaciones:
        # Crear copia del dataframe para no modificar el original
        datos_normalizados = datos.copy()
        
        # Aplicar la normalización a la columna 'Teaser Text'
        datos_normalizados['Teaser Text'] = datos_normalizados['Teaser Text'].apply(
            lambda x: norm_func.normalizar(x, nlp)
        )
        
        # Guardar el corpus normalizado
        ruta_guardado = os.path.join(f'corpus/normalizacion{num}', f'CorpusNormalizado{num}.csv')
        datos_normalizados.to_csv(ruta_guardado, index=False)
        
        print(f"Corpus con normalización {num} guardado en {ruta_guardado}")

def main():
    # Cargar datos
    datos = cargar_datos()
    
    # Aplicar normalizaciones y guardar los resultados
    aplicar_normalizacion_y_guardar(datos)

if __name__ == "__main__":
    main()