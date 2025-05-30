# ================================
# CELDA 1: INSTALACIÓN Y CONFIGURACIÓN
# ================================

# Instalar librerías necesarias
!pip install transformers datasets accelerate -q
!pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 -q

# Verificar GPU
import torch
print(f"CUDA disponible: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"Memoria GPU: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")

# ================================
# CELDA 2: SUBIR ARCHIVOS
# ================================

from google.colab import files
import os

print("SUBE LOS ARCHIVOS CSV:")
print("1. TA1C_dataset_detection_train.csv")
print("2. TA1C_dataset_detection_dev.csv (opcional para predicciones finales)")

# Subir archivos
uploaded = files.upload()

# Verificar archivos subidos
for filename in uploaded.keys():
    print(f"Archivo subido: {filename} ({len(uploaded[filename])} bytes)")

# ================================
# CELDA 3: CÓDIGO PRINCIPAL - SOLO BERT
# ================================

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, f1_score
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    DataCollatorWithPadding
)
from torch.utils.data import Dataset
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import transformers
warnings.filterwarnings('ignore')

# Configuración
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Usando device: {device}")
print(f"Versión de transformers: {transformers.__version__}")

class ClickbaitDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length=512):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = str(self.texts[idx])
        label = self.labels[idx]

        encoding = self.tokenizer(
            text,
            truncation=True,
            padding='max_length',
            max_length=self.max_length,
            return_tensors='pt'
        )

        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }

def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    f1_macro = f1_score(labels, predictions, average='macro')
    return {'f1_macro': f1_macro}

# ================================
# CELDA 4: CARGAR Y PROCESAR DATOS
# ================================

print("=== CARGANDO DATOS ===")

# Cargar corpus
df_train = pd.read_csv('TA1C_dataset_detection_train.csv')
print(f"📊 Corpus cargado: {len(df_train)} instancias")
print(f"📋 Columnas: {df_train.columns.tolist()}")
print(f"🏷️ Distribución de clases:")
print(df_train['Tag Value'].value_counts())

# Preparar datos
X = df_train['Teaser Text'].values
y = df_train['Tag Value'].values

# Convertir etiquetas a números si son texto
if y.dtype == 'object':
    unique_labels = np.unique(y)
    label_map = {label: idx for idx, label in enumerate(unique_labels)}
    y = np.array([label_map[label] for label in y])
    print(f"🔢 Mapeo de etiquetas: {label_map}")

# División train-dev
X_train, X_dev, y_train, y_dev = train_test_split(
    X, y,
    test_size=0.25,
    random_state=0,
    shuffle=True,
    stratify=y
)

print(f"🚂 Train set: {len(X_train)} instancias")
print(f"🔍 Dev set: {len(X_dev)} instancias")

# ================================
# CELDA 5: ENTRENAR BERT
# ================================

print("🚀 ENTRENANDO BERT...")

# Configuración específica para BERT
model_name = 'bert-base-uncased'

# Tokenizer
print("📝 Cargando tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Crear datasets
print("📊 Creando datasets...")
train_dataset = ClickbaitDataset(X_train, y_train, tokenizer)
eval_dataset = ClickbaitDataset(X_dev, y_dev, tokenizer)

# Cargar modelo
print("🤖 Cargando modelo BERT...")
model = AutoModelForSequenceClassification.from_pretrained(
    model_name,
    num_labels=2,
    ignore_mismatched_sizes=True
)
model.to(device)

# Configurar argumentos de entrenamiento (optimizados para BERT en Colab)
training_args = TrainingArguments(
    output_dir='/content/bert_model',
    num_train_epochs=2,  # Reducido para Colab
    per_device_train_batch_size=8,  # Batch pequeño para modelo grande
    per_device_eval_batch_size=8,
    learning_rate=2e-5,  # LR específico para BERT
    weight_decay=0.01,
    logging_steps=50,
    eval_strategy='steps',
    eval_steps=100,
    save_strategy='steps',
    save_steps=100,
    save_total_limit=1,
    load_best_model_at_end=True,
    metric_for_best_model='f1_macro',
    greater_is_better=True,
    report_to=None,
    dataloader_pin_memory=False,
)

# Data collator
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
)

# Entrenar
print("🏋️‍♂️ Iniciando entrenamiento...")
trainer.train()

# ================================
# CELDA 6: EVALUACIÓN
# ================================

print("📊 EVALUANDO MODELO...")

# Predicciones en dev set
predictions = trainer.predict(eval_dataset)
y_pred = np.argmax(predictions.predictions, axis=1)

# Calcular F1-macro
f1_macro = f1_score(y_dev, y_pred, average='macro')
print(f"✅ F1-macro: {f1_macro:.4f}")

# Reporte detallado
print(f"\n📋 REPORTE DE CLASIFICACIÓN:")
print(classification_report(y_dev, y_pred))

# Matriz de confusión
cm = confusion_matrix(y_dev, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar_kws={'shrink': 0.8})
plt.title('Matriz de Confusión - BERT')
plt.ylabel('Etiqueta Real')
plt.xlabel('Etiqueta Predicha')
plt.tight_layout()
plt.show()

# ================================
# CELDA 7: PREDICCIONES FINALES (OPCIONAL)
# ================================

# Solo ejecutar si tienes el archivo de test
if 'TA1C_dataset_detection_dev.csv' in [f for f in os.listdir('.') if f.endswith('.csv')]:
    print(f"\n🔮 GENERANDO PREDICCIONES FINALES...")

    try:
        # Cargar test set
        df_test = pd.read_csv('TA1C_dataset_detection_dev.csv')
        print(f"📊 Test set: {len(df_test)} instancias")

        # Preparar datos
        X_test = df_test['Teaser Text'].values
        test_ids = df_test['Tweet ID'].values if 'Tweet ID' in df_test.columns else range(len(df_test))

        # Dataset dummy
        dummy_labels = [0] * len(X_test)
        test_dataset = ClickbaitDataset(X_test, dummy_labels, tokenizer)

        # Predicciones
        predictions = trainer.predict(test_dataset)
        y_pred_test = np.argmax(predictions.predictions, axis=1)

        # Crear CSV
        results_df = pd.DataFrame({
            'Tweet ID': test_ids,
            'Tag Value': y_pred_test
        })

        results_df.to_csv('detection_bert.csv', index=False)
        print("✅ Archivo 'detection_bert.csv' generado!")

        # Descargar archivo
        files.download('detection_bert.csv')

    except Exception as e:
        print(f"❌ Error generando predicciones: {e}")

print(f"\n🎉 ¡ENTRENAMIENTO DE BERT COMPLETADO!")
print(f"🏆 F1-macro final: {f1_macro:.4f}")

# Limpiar memoria
del trainer, model
torch.cuda.empty_cache()
print("🧹 Memoria GPU liberada")
