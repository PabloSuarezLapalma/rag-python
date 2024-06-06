import json

# Leer el archivo de texto
with open('Reglamentacion.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Procesar el contenido del archivo
data = []
current_content = []
for line in lines:
    stripped_line = line.strip()

    if stripped_line.startswith('Capitulo') or stripped_line.startswith('Articulo'):
        if current_content:
            # Unir las líneas de la sección y agregar al dataset
            content = " ".join(current_content).strip()
            if content:
                data.append({"role": "user", "content": content})
            current_content = []

    if stripped_line:
        current_content.append(stripped_line)

# Agregar la última sección si existe
if current_content:
    content = " ".join(current_content).strip()
    if content:
        data.append({"role": "user", "content": content})

# Convertir la lista de secciones en formato JSON
json_data = json.dumps(data, ensure_ascii=False, indent=4)

# Guardar el JSON en un archivo
with open('dataset.json', 'w', encoding='utf-8') as json_file:
    json_file.write(json_data)

print("Archivo JSON creado con éxito.")
