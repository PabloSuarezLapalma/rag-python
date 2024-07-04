import json
import os
from datasets import Dataset, DatasetDict
from dotenv import load_dotenv
from huggingface_hub import HfApi, HfFolder


#NOTA: Esta función para transformar el dataset utiliza como dataset base el formato utilizado en SQUAD v1 y v2.
# Que sigue la siguiente forma (es un array de varios elementos como siguen):
# {
#         "id": "1",
#         "title": "Titulo del documento",
#         "context": "Contexto del documento",
#         "question": "Pregunta",
#         "answers": {
#             "text": [
#                 "Respuesta"
#             ],
#             "answer_start": [
#                 0 #nro que indica el inicio de la respuesta
#             ]
#         }
#     }

#Según sea necesario para el dataset disponible se deberá modificar para que los campos correspondan a los datos que se tienen.

#Carga de los datos desde un archivo en formato Pregunta-Respuesta obtenido como respuesta de Ollama desde la PC del GIBD

def transformar_dataset2(lineas):
    transformado = []
    
    # Verificar si el número de líneas es par
    if len(lineas) % 2 != 0:
        raise ValueError("El archivo no tiene un número par de líneas. Cada pregunta debe tener una respuesta correspondiente.")
    
    # Asumiendo que el formato del archivo es alternado: Pregunta, Respuesta, Pregunta, Respuesta...
    for i in range(0, len(lineas), 2):
        try:
            pregunta_linea = lineas[i].strip()
            respuesta_linea = lineas[i + 1].strip()
            
            # Remover los prefijos 'Pregunta: ' y 'Respuesta: '
            if not pregunta_linea.startswith("Pregunta: ") or not respuesta_linea.startswith("Respuesta: "):
                raise ValueError(f"Formato incorrecto en las líneas {i+1} y {i+2}.")
            
            pregunta = pregunta_linea.replace("Pregunta: ", "")
            respuesta = respuesta_linea.replace("Respuesta: ", "")
            
            transformado.append({
                "conversations": [
                    {"from": "human", "value": pregunta},
                    {"from": "gpt", "value": respuesta}
                ]
            })
        except IndexError:
            raise IndexError(f"Error al acceder a las líneas {i} y {i+1}. Verifique que el archivo tenga un número par de líneas y el formato correcto.")
    
    return transformado

### Cargar los datos desde los archivos en formato SQuAD

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

with open("PreguntasRespuestasGPT4o.txt", 'r', encoding='utf-8') as archivo:
    lineas = archivo.readlines()
        

# Transformar los datasets
#train_data_transformado = transformar_dataset(train_data)
train_data_transformado = transformar_dataset2(lineas)

#validation_data_transformado = transformar_dataset(validation_data)
validation_data_transformado = transformar_dataset2(lineas)


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

# Estos datos deben ser ingresados por medio de un archivo .env que contenga las variables de entorno aquí citadas
hf_user= os.getenv('HF_USER')
hf_token = os.getenv('HF_TOKEN')
hf_repository= os.getenv('HF_REPOSITORY_NAME')

if hf_token is None:
    raise ValueError("La variable de entorno HF_TOKEN no está establecida.")

# Autenticación y subida a Hugging Face
HfFolder.save_token(hf_token)
api = HfApi()


repo_name = hf_user+"/"+hf_repository

# Crear un nuevo repositorio en Hugging Face
api.create_repo(repo_id=repo_name, repo_type="dataset", private=False)

# Subir el dataset al repositorio
dataset_dict.push_to_hub(repo_id=repo_name)
