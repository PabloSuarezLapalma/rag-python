import json
import os
from datasets import Dataset, DatasetDict
from dotenv import load_dotenv
from huggingface_hub import HfApi, HfFolder

def transformar_dataset(data):
    transformado = []
    for item in data:
        transformado.append({
            "conversations": [
                {"from": "human", "value": item["question"]},
                {"from": "gpt", "value": item["answers"]["text"][0]}
            ]
        })
    return transformado

# Cargar los datos desde los archivos JSON
with open("train.json", "r", encoding="utf-8") as f:
    train_data = json.load(f)

with open("validation.json", "r", encoding="utf-8") as f:
    validation_data = json.load(f)

# Transformar los datasets
train_data_transformado = transformar_dataset(train_data)
validation_data_transformado = transformar_dataset(validation_data)

# Guardar los datasets transformados a archivos JSON
with open("train_transformado.json", "w", encoding="utf-8") as f:
    json.dump(train_data_transformado, f, ensure_ascii=False, indent=2)

with open("validation_transformado.json", "w", encoding="utf-8") as f:
    json.dump(validation_data_transformado, f, ensure_ascii=False, indent=2)

# Función para convertir lista de diccionarios a diccionario de listas
def list_of_dicts_to_dict_of_lists(data):
    dict_of_lists = {key: [dic[key] for dic in data] for key in data[0]}
    return dict_of_lists

# Convertir los datos transformados
train_data_dict = list_of_dicts_to_dict_of_lists(train_data_transformado)
validation_data_dict = list_of_dicts_to_dict_of_lists(validation_data_transformado)

# Crear datasets de Hugging Face
train_dataset = Dataset.from_dict(train_data_dict)
validation_dataset = Dataset.from_dict(validation_data_dict)

# Crear un DatasetDict con las divisiones train y validation
dataset_dict = DatasetDict({
    "train": train_dataset,
    "validation": validation_dataset
})

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener el valor de la variable de entorno
hf_token = os.getenv('HF_TOKEN')

if hf_token is None:
    raise ValueError("La variable de entorno HF_TOKEN no está establecida.")

# Autenticación y subida a Hugging Face
HfFolder.save_token(hf_token)
api = HfApi()

# Nombre del repositorio de dataset en Hugging Face
repo_name = "P4B10/reglamentacion-alpha"  # Reemplaza "tu_usuario" con tu nombre de usuario en Hugging Face

# Crear un nuevo repositorio en Hugging Face
api.create_repo(repo_id=repo_name, repo_type="dataset", private=False)

# Subir el dataset al repositorio
dataset_dict.push_to_hub(repo_id=repo_name)
