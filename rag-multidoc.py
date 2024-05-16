import ollama
import os
import json
import numpy as np
from numpy.linalg import norm
from concurrent.futures import ThreadPoolExecutor
import logging
from pathlib import Path
import fitz  # PyMuPDF

ollama_model = "mistral"
file_Name = "Rules_en"
embedding_model = "nomic-embed-text"

#Non functional with pdfs yet

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_txt(filename):
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

def parse_pdf(filename):
    doc = fitz.open(filename)
    paragraphs = []
    buffer = []
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text = page.get_text("text")
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if line:
                buffer.append(line)
            elif buffer:
                paragraphs.append(" ".join(buffer))
                buffer = []
        if buffer:
            paragraphs.append(" ".join(buffer))
            buffer = []
    return paragraphs

def parse_file(filename):
    if filename.endswith('.txt'):
        return parse_txt(filename)
    elif filename.endswith('.pdf'):
        return parse_pdf(filename)
    else:
        raise ValueError("Unsupported file format. Please use .txt or .pdf files.")

def save_embeddings(filename, embeddings):
    Path("embeddings").mkdir(exist_ok=True)
    np.save(f"embeddings/{filename}.npy", embeddings)

def load_embeddings(filename):
    filepath = Path(f"embeddings/{filename}.npy")
    if not filepath.exists():
        return None
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
    filename = file_Name
    file_path = f"{filename}.txt" if Path(f"{filename}.txt").exists() else f"{filename}.pdf"
    paragraphs = parse_file(file_path)

    embeddings = get_embeddings(filename, embedding_model, paragraphs)

    conversation_history = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    while True:
        prompt = input(">>> Qué quieres saber?:  ")
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

        conversation_history.append({"role": "assistant", "content": response_content})

if __name__ == "__main__":
    main()
