import json

# Abre el archivo JSON
with open('database.json') as json_file:
    datos = json.load(json_file)

if isinstance(datos, list):
    for item in datos:
        if not isinstance(item, dict):
            print("El elemento no es un diccionario:", item)
else:
    print("Los datos no son una lista.")
