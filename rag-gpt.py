import ollama
import os
import json
import numpy as np
from numpy.linalg import norm
from concurrent.futures import ThreadPoolExecutor
import logging
from pathlib import Path

#Change for fine-tuning the model

ollama_model="llama3"
file_Name="Reglamentacion"
embedding_model="nomic-embed-text"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# open a file and return paragraphs
def parse_file(filename):
    with open(filename, encoding="utf-8-sig") as f:
        paragraphs = []
        buffer = []
        for line in f.readlines():
            line = line.strip()
            if line:
                buffer.append(line)
            elif buffer:
                paragraphs.append(" ".join(buffer))
                buffer = []
        if buffer:
            paragraphs.append(" ".join(buffer))
        return paragraphs

def save_embeddings(filename, embeddings):
    # create dir if it doesn't exist
    Path("embeddings").mkdir(exist_ok=True)
    # save embeddings to npy file
    np.save(f"embeddings/{filename}.npy", embeddings)

def load_embeddings(filename):
    filepath = Path(f"embeddings/{filename}.npy")
    if not filepath.exists():
        return None
    # load embeddings from npy file
    return np.load(filepath, allow_pickle=True).tolist()

def get_embeddings(filename, modelname, chunks):
    embeddings = load_embeddings(filename)
    if embeddings is not None:
        return embeddings
    logger.info("Generating embeddings...")
    with ThreadPoolExecutor() as executor:
        embeddings = list(executor.map(lambda chunk: ollama.embeddings(model=modelname, prompt=chunk)["embedding"], chunks))
    save_embeddings(filename, embeddings)
    return embeddings

# find cosine similarity of every chunk to a given embedding
def find_most_similar(needle, haystack):
    needle_norm = norm(needle)
    similarity_scores = [
        np.dot(needle, item) / (needle_norm * norm(item)) for item in haystack
    ]
    return sorted(zip(similarity_scores, range(len(haystack))), reverse=True)

def main():
    SYSTEM_PROMPT= """You are a helpful reading assistant who answers questions 
    based on snippets of text provided in context. Answer only using the context provided, 
    being as concise as possible. If you're unsure, just say that you don't know.
    Context:
    """
    SYSTEM_PROMPT2=""" Eres un modelo de lenguaje especializado en proporcionar información y aclaraciones sobre regulaciones académicas. Tu objetivo es asistir a los usuarios respondiendo sus preguntas de manera precisa y concisa conforme a la normativa académica estándar.

Instrucciones para el modelo:

Responde de manera clara y precisa, basándote en las regulaciones académicas comunes.
En caso de que la pregunta no esté cubierta por las normativas estándar, indica que la información específica no está disponible.
Mantén un tono formal y profesional.
Si es relevante, proporciona ejemplos para clarificar puntos específicos.
Asegúrate de ser coherente y evitar contradicciones en tus respuestas."""
    # open file
    filename = file_Name
    paragraphs = parse_file(f"{filename}.txt")

    embeddings = get_embeddings(filename, embedding_model, paragraphs)

    conversation_history = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    while True:
        prompt = input(">>> Pregunta:  ")
        if not prompt.strip():
            print("Exiting...")
            break

        prompt_embedding = ollama.embeddings(model=embedding_model, prompt=prompt)["embedding"]

        most_similar_chunks = find_most_similar(prompt_embedding, embeddings)[:5]

        context = "\n".join(paragraphs[item[1]] for item in most_similar_chunks)
        conversation_history.append({"role": "user", "content": prompt})
        conversation_history.append({"role": "system", "content": SYSTEM_PROMPT + context})

        response = ollama.chat(
            model=ollama_model,
            messages=conversation_history,
        )
        response_content = response["message"]["content"]
        print("\n\n")
        print(response_content)

        # Add the assistant's response to the conversation history
        conversation_history.append({"role": "assistant", "content": response_content})

if __name__ == "__main__":
    main()
