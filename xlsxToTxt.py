import pandas as pd

# Nombre del archivo de entrada y salida
input_file = 'dataset.xls'
output_file = 'dataset_reglamentacion.txt'

# Lee el archivo XLS
df = pd.read_excel(input_file, engine='xlrd')

# Escribe el contenido del DataFrame en un archivo TXT
df.to_csv(output_file, sep='\t', index=False)

print(f'Archivo TXT guardado como {output_file}')
