import ollama
import os
import json
import numpy as np
from numpy.linalg import norm
from concurrent.futures import ThreadPoolExecutor
import logging
from pathlib import Path
from tranformers import AutoTokenizer

ollama_model="mistral"
file="Reglamentacion.txt"
embedding_model="nomic-embed-text"

# Log Set-Up
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#Opens the file for fine-tuning
with open(file, 'r', encoding='utf-8') as f:
    text = f.read()

