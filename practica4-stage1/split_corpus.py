import os
import pandas as pd
from sklearn.model_selection import train_test_split

def limpiar_saltos_linea(texto):
    """Reemplaza saltos de línea y retornos de carro por espacios"""
    if isinstance(texto, str):
        return texto.replace('\n', ' ').replace('\r', ' ')
    return texto

def dividir_corpus_en_train_dev():
    # Iterar sobre las 5 normalizaciones
    for i in range(1, 6):
        # Rutas de los archivos
        carpeta = f'corpus/normalizacion{i}'
        archivo_entrada = os.path.join(carpeta, f'CorpusNormalizado{i}.csv')
        
        # Cargar el corpus normalizado
        datos = pd.read_csv(archivo_entrada)
        
        # Limpiar saltos de línea en 'Teaser Text'
        datos['Teaser Text'] = datos['Teaser Text'].apply(limpiar_saltos_linea)
        
        # Separar características (X) y etiquetas (y)
        X = datos['Teaser Text']
        y = datos['Tag Value']
        
        # Dividir el corpus (75% train, 25% dev)
        X_train, X_dev, y_train, y_dev = train_test_split(
            X, y,
            test_size=0.25,
            shuffle=True,
            random_state=0,
            stratify=y
        )
        
        # Crear dataframes para train y dev
        train_df = datos.loc[X_train.index]
        dev_df = datos.loc[X_dev.index]
        
        # Configuración adicional para pandas.to_csv
        csv_config = {
            'index': False,
            'encoding': 'utf-8',
            'quotechar': '"',
            'quoting': 1  # QUOTE_MINIMAL
        }
        
        # Guardar los conjuntos train y dev
        train_df.to_csv(os.path.join(carpeta, f'train_{i}.csv'), **csv_config)
        dev_df.to_csv(os.path.join(carpeta, f'dev_{i}.csv'), **csv_config)
        
        print(f"Normalización {i}:")
        print(f"  - Conjunto de entrenamiento guardado en: {os.path.join(carpeta, f'train_{i}.csv')}")
        print(f"  - Conjunto de desarrollo guardado en: {os.path.join(carpeta, f'dev_{i}.csv')}")
        print(f"  - Tamaño original: {len(datos)} instancias")
        print(f"  - Train: {len(train_df)} instancias (75%)")
        print(f"  - Dev: {len(dev_df)} instancias (25%)")
        print("  - Proporción de clases en train:", y_train.value_counts(normalize=True).to_dict())
        print("  - Proporción de clases en dev:", y_dev.value_counts(normalize=True).to_dict())
        print()

if __name__ == "__main__":
    dividir_corpus_en_train_dev()