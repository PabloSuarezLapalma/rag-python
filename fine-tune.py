import ollama
import os
import json
import numpy as np
from numpy.linalg import norm
from concurrent.futures import ThreadPoolExecutor
import logging
from pathlib import Path
from transformers import AutoTokenizer

ollama_model="mistral"
file="Reglamentacion.txt"
prompt="¿Cuáles son las responsabilidades del Decano?"
# Log Set-Up
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#Opens the file for fine-tuning
with open(file, 'r', encoding='utf-8') as f:
    text = f.read()

#Ollama basic usage
stream = ollama.chat(
    model=ollama_model,
    messages=[{'role': 'user', 'content': prompt}],
    stream=True,
)

for chunk in stream:
  print(chunk['message']['content'], end='', flush=True)

