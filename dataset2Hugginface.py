import json
import os
from datasets import Dataset, DatasetDict
from dotenv import load_dotenv

# Cargar los datos desde los archivos JSON
with open("train.json", "r", encoding="utf-8") as f:
    train_data = json.load(f)

with open("validation.json", "r", encoding="utf-8") as f:
    validation_data = json.load(f)

# Función para convertir lista de diccionarios a diccionario de listas
def list_of_dicts_to_dict_of_lists(data):
    dict_of_lists = {key: [dic[key] for dic in data] for key in data[0]}
    return dict_of_lists

# Convertir los datos
train_data_dict = list_of_dicts_to_dict_of_lists(train_data)
validation_data_dict = list_of_dicts_to_dict_of_lists(validation_data)

# Crear datasets de Hugging Face
train_dataset = Dataset.from_dict(train_data_dict)
validation_dataset = Dataset.from_dict(validation_data_dict)

# Crear un DatasetDict con las divisiones train y validation
dataset_dict = DatasetDict({
    "train": train_dataset,
    "validation": validation_dataset
})

#NOTA: se debe definir el HF_TOKEN en un archivo dentro del repositorio que se llama .env solamente
# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Especifica tu token de acceso de Hugging Face
hf_token = os.getenv('HF_TOKEN')

if hf_token is None:
    raise ValueError("La variable de entorno HF_TOKEN no está establecida.")

# Autenticación y subida a Hugging Face
from huggingface_hub import HfApi, HfFolder
HfFolder.save_token(hf_token)
api = HfApi()

# Nombre del repositorio de dataset en Hugging Face
repo_name = "P4B10/reglamentacion-beta"  # Reemplaza "tu_usuario" con tu nombre de usuario en Hugging Face

# Crear un nuevo repositorio en Hugging Face
api.create_repo(repo_id=repo_name, repo_type="dataset", private=False)

# Subir el dataset al repositorio
dataset_dict.push_to_hub(repo_id=repo_name)
