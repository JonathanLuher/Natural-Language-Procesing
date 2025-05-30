import os
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report, f1_score
from time import time
from sklearn.utils.validation import check_X_y

def load_data(norm_number, set_type='dev'):
    """Carga los datos de desarrollo o entrenamiento"""
    path = os.path.join('corpus', f'normalizacion{norm_number}', f'{set_type}_{norm_number}.csv')
    df = pd.read_csv(path)
    return df

def load_representation(norm_number, rep_name):
    """Carga la representación transformada"""
    rep_folder = os.path.join('corpus', f'normalizacion{norm_number}', 'RepresentacionesTrain')
    
    # Cargar el transformador
    pipeline_path = os.path.join(rep_folder, f'{rep_name}_fold1.pkl')
    pipeline = joblib.load(pipeline_path)
    
    # Cargar datos de entrenamiento transformados
    train_path = os.path.join(rep_folder, f'{rep_name}_fold1.csv')
    train_df = pd.read_csv(train_path)
    
    # Seleccionar solo columnas de características generadas (feature_*)
    feature_cols = [col for col in train_df.columns if col.startswith('feature_')]
    X_train = train_df[feature_cols].astype(float)
    y_train = train_df['Tag Value']
    
    return pipeline, X_train, y_train

def prepare_dev_data(dev_df, pipeline):
    """Transforma los datos de desarrollo usando el pipeline"""
    try:
        # Eliminar columnas no necesarias antes de transformar
        cols_to_drop = ['Tweet ID', 'Tweet Date', 'Media Name', 'Media Origin', 'Tag Value']
        cols_to_drop = [col for col in cols_to_drop if col in dev_df.columns]
        
        # Conservar solo el texto para transformar
        if 'Teaser Text' in dev_df.columns:
            X_dev = dev_df['Teaser Text']
        else:
            X_dev = dev_df.drop(columns=cols_to_drop)
        
        # Transformar usando el pipeline
        X_dev_transformed = pipeline.transform(X_dev)
        X_dev = pd.DataFrame(X_dev_transformed, 
                           columns=[f'feature_{i}' for i in range(X_dev_transformed.shape[1])])
        y_dev = dev_df['Tag Value']
        return X_dev, y_dev
    except Exception as e:
        raise ValueError(f"Error transformando datos de desarrollo: {str(e)}")

def setup_models():
    """Configura los modelos y sus parámetros para GridSearch"""
    return {
        'LogisticRegression': {
            'clf': LogisticRegression(max_iter=1000, random_state=0),
            'params': {'C': [0.1, 1, 10], 'penalty': ['l2']}
        },
        'SVM': {
            'clf': SVC(random_state=0),
            'params': {'C': [0.1, 1, 10], 'kernel': ['linear', 'rbf']}
        },
        'RandomForest': {
            'clf': RandomForestClassifier(random_state=0),
            'params': {'n_estimators': [50, 100], 'max_depth': [None, 10, 20]}
        },
        'GradientBoosting': {
            'clf': GradientBoostingClassifier(random_state=0),
            'params': {'n_estimators': [50, 100], 'learning_rate': [0.01, 0.1], 'max_depth': [3, 5]}
        }
    }

def train_and_evaluate():
    """Función principal para entrenar y evaluar modelos"""
    models = setup_models()
    
    for norm_num in range(1, 6):  # Para cada normalización (1-5)
        print(f"\n{'='*50}")
        print(f"PROCESANDO NORMALIZACIÓN {norm_num}")
        print(f"{'='*50}")
        
        # Preparar carpeta para modelos
        model_folder = os.path.join('corpus', f'normalizacion{norm_num}', 'Modelos')
        os.makedirs(model_folder, exist_ok=True)
        
        # Cargar datos de desarrollo originales
        dev_df = load_data(norm_num, 'dev')
        
        # Obtener lista de representaciones
        rep_folder = os.path.join('corpus', f'normalizacion{norm_num}', 'RepresentacionesTrain')
        representations = set(f.replace('_fold1.pkl', '') 
                            for f in os.listdir(rep_folder) 
                            if f.endswith('_fold1.pkl'))
        
        for rep_name in representations:
            print(f"\nEvaluando representación: {rep_name}")
            
            try:
                # Cargar representación y datos de entrenamiento
                pipeline, X_train, y_train = load_representation(norm_num, rep_name)
                
                # Transformar datos de desarrollo
                X_dev, y_dev = prepare_dev_data(dev_df, pipeline)
                
                # Verificar datos
                X_train, y_train = check_X_y(X_train, y_train)
                X_dev, y_dev = check_X_y(X_dev, y_dev)
                
            except Exception as e:
                print(f"Error preparando datos: {str(e)}")
                continue
            
            # Entrenar y evaluar cada modelo
            for model_name, config in models.items():
                print(f"  Entrenando {model_name}...")
                start_time = time()
                
                try:
                    # Configurar GridSearchCV
                    grid_search = GridSearchCV(
                        estimator=config['clf'],
                        param_grid=config['params'],
                        cv=5,
                        scoring='f1_macro',
                        n_jobs=-1,
                        verbose=0
                    )
                    
                    # Entrenar modelo
                    grid_search.fit(X_train, y_train)
                    
                    # Evaluar
                    y_pred = grid_search.predict(X_dev)
                    f1 = f1_score(y_dev, y_pred, average='macro')
                    
                    # Guardar modelo
                    model_path = os.path.join(model_folder, f"{rep_name}_{model_name}.pkl")
                    joblib.dump(grid_search.best_estimator_, model_path)
                    
                    # Guardar reporte
                    report = classification_report(y_dev, y_pred, output_dict=True)
                    report_path = os.path.join(model_folder, f"{rep_name}_{model_name}_report.csv")
                    pd.DataFrame(report).transpose().to_csv(report_path)
                    
                    # Guardar parámetros
                    params_path = os.path.join(model_folder, f"{rep_name}_{model_name}_params.txt")
                    with open(params_path, 'w') as f:
                        f.write(str(grid_search.best_params_))
                    
                    print(f"    Mejor F1-score: {f1:.4f}")
                    print(f"    Mejores parámetros: {grid_search.best_params_}")
                    print(f"    Modelo guardado en: {model_path}")
                    print(f"    Tiempo total: {time()-start_time:.2f} segundos")
                
                except Exception as e:
                    print(f"    Error entrenando {model_name}: {str(e)}")
                    continue

if __name__ == "__main__":
    train_and_evaluate()