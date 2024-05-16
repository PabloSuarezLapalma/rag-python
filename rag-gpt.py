import ollama
import os
import json
import numpy as np
from numpy.linalg import norm
from concurrent.futures import ThreadPoolExecutor
import logging
from pathlib import Path

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
    SYSTEM_PROMPT = """You are a helpful reading assistant who answers questions 
    based on snippets of text provided in context. Answer only using the context provided, 
    being as concise as possible. If you're unsure, just say that you don't know.
    Context:
    """
    # open file
    filename = "Reglamentacion"
    paragraphs = parse_file(f"{filename}.txt")

    embeddings = get_embeddings(filename, "nomic-embed-text", paragraphs)

    conversation_history = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    while True:
        prompt = input("What do you want to know? -> ")
        if not prompt.strip():
            print("Exiting...")
            break

        prompt_embedding = ollama.embeddings(model="nomic-embed-text", prompt=prompt)["embedding"]

        most_similar_chunks = find_most_similar(prompt_embedding, embeddings)[:5]

        context = "\n".join(paragraphs[item[1]] for item in most_similar_chunks)
        conversation_history.append({"role": "user", "content": prompt})
        conversation_history.append({"role": "system", "content": SYSTEM_PROMPT + context})

        response = ollama.chat(
            model="llama3",
            messages=conversation_history,
        )
        response_content = response["message"]["content"]
        print("\n\n")
        print(response_content)

        # Add the assistant's response to the conversation history
        conversation_history.append({"role": "assistant", "content": response_content})

if __name__ == "__main__":
    main()
