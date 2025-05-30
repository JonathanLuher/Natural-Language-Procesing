import os
import pandas as pd
import joblib
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import Pipeline

def limpiar_saltos_linea(texto):
    """Reemplaza saltos de línea y retornos de carro por espacios"""
    if pd.isna(texto):  # Manejar valores NaN
        return ""
    if isinstance(texto, str):
        return texto.replace('\n', ' ').replace('\r', ' ')
    return str(texto)  # Convertir otros tipos a string por si acaso

def crear_representaciones_texto():
    # Configuración común para guardar CSV
    csv_config = {
        'index': False,
        'encoding': 'utf-8',
        'quotechar': '"',
        'quoting': 1  # QUOTE_MINIMAL
    }
    
    # Iterar sobre las 5 normalizaciones
    for i in range(1, 6):
        print(f"\nProcesando normalización {i}...")
        
        # Rutas de los archivos
        carpeta = f'corpus/normalizacion{i}'
        archivo_train = os.path.join(carpeta, f'train_{i}.csv')
        carpeta_representaciones = os.path.join(carpeta, "RepresentacionesTrain")
        
        # Crear carpeta si no existe
        os.makedirs(carpeta_representaciones, exist_ok=True)
        
        # Cargar datos de entrenamiento
        train_df = pd.read_csv(archivo_train)
        
        # Limpiar y manejar NaN en 'Teaser Text'
        train_df['Teaser Text'] = train_df['Teaser Text'].apply(limpiar_saltos_linea)
        
        # Verificar si hay textos vacíos después de la limpieza
        empty_texts = train_df['Teaser Text'].str.strip() == ""
        if empty_texts.any():
            print(f"  Advertencia: {empty_texts.sum()} textos están vacíos después de limpieza")
        
        X_train = train_df['Teaser Text']
        y_train = train_df['Tag Value']
        
        # Configuraciones de representación a probar
        representaciones = [
            # Unigramas
            {'nombre': 'unigram_binary', 'vectorizer': CountVectorizer(binary=True, ngram_range=(1,1))},
            {'nombre': 'unigram_freq', 'vectorizer': CountVectorizer(binary=False, ngram_range=(1,1))},
            {'nombre': 'unigram_tfidf', 'vectorizer': TfidfVectorizer(ngram_range=(1,1))},
            
            # Bigramas
            {'nombre': 'bigram_binary', 'vectorizer': CountVectorizer(binary=True, ngram_range=(2,2))},
            {'nombre': 'bigram_freq', 'vectorizer': CountVectorizer(binary=False, ngram_range=(2,2))},
            {'nombre': 'bigram_tfidf', 'vectorizer': TfidfVectorizer(ngram_range=(2,2))},
            
            # Trigramas
            {'nombre': 'trigram_binary', 'vectorizer': CountVectorizer(binary=True, ngram_range=(3,3))},
            {'nombre': 'trigram_freq', 'vectorizer': CountVectorizer(binary=False, ngram_range=(3,3))},
            {'nombre': 'trigram_tfidf', 'vectorizer': TfidfVectorizer(ngram_range=(3,3))},
            
            # Combinaciones
            {'nombre': 'uni_bi_gram_binary', 'vectorizer': CountVectorizer(binary=True, ngram_range=(1,2))},
            {'nombre': 'uni_bi_gram_freq', 'vectorizer': CountVectorizer(binary=False, ngram_range=(1,2))},
            {'nombre': 'uni_bi_gram_tfidf', 'vectorizer': TfidfVectorizer(ngram_range=(1,2))},
            
            {'nombre': 'uni_bi_tri_gram_binary', 'vectorizer': CountVectorizer(binary=True, ngram_range=(1,3))},
            {'nombre': 'uni_bi_tri_gram_freq', 'vectorizer': CountVectorizer(binary=False, ngram_range=(1,3))},
            {'nombre': 'uni_bi_tri_gram_tfidf', 'vectorizer': TfidfVectorizer(ngram_range=(1,3))},
        ]
        
        # Aplicar validación cruzada estratificada de 5 folds
        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
        
        for config in representaciones:
            print(f"  Procesando representación: {config['nombre']}")
            
            try:
                # Crear pipeline con posible reducción de dimensionalidad
                pipeline = Pipeline([
                    ('vectorizer', config['vectorizer']),
                    ('svd', TruncatedSVD(n_components=100, random_state=0))  # Reducción a 100 componentes
                ])
                
                # Aplicar validación cruzada
                for fold, (train_idx, val_idx) in enumerate(skf.split(X_train, y_train)):
                    # Entrenar el pipeline con el fold de entrenamiento
                    X_train_fold = X_train.iloc[train_idx]
                    pipeline.fit(X_train_fold, y_train.iloc[train_idx])  # Añadido y_train para fitting
                    
                    # Transformar todo el conjunto de entrenamiento
                    X_transformed = pipeline.transform(X_train)
                    
                    # Crear dataframe con las características
                    features_df = pd.DataFrame(X_transformed, 
                                             columns=[f"feature_{i}" for i in range(X_transformed.shape[1])])
                    
                    # Combinar con las columnas originales (excepto 'Teaser Text')
                    result_df = pd.concat([
                        train_df.drop(columns=['Teaser Text']),
                        features_df
                    ], axis=1)
                    
                    # Guardar resultados para este fold
                    nombre_archivo = f"{config['nombre']}_fold{fold+1}.csv"
                    ruta_guardado = os.path.join(carpeta_representaciones, nombre_archivo)
                    result_df.to_csv(ruta_guardado, **csv_config)
                    
                    # Guardar también el modelo/pipeline para este fold
                    nombre_modelo = f"{config['nombre']}_fold{fold+1}.pkl"
                    ruta_modelo = os.path.join(carpeta_representaciones, nombre_modelo)
                    joblib.dump(pipeline, ruta_modelo)
                
                print(f"  Representación {config['nombre']} completada - 5 folds generados")
            
            except Exception as e:
                print(f"  Error procesando {config['nombre']}: {str(e)}")
                continue

if __name__ == "__main__":
    crear_representaciones_texto()