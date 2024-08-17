import ollama
import numpy as np
from numpy.linalg import norm
from concurrent.futures import ThreadPoolExecutor
import logging
from pathlib import Path

ollama_model='gemma2:2b'
file_Name="Reglamentacion"
embedding_model="bge-m3"

# Si desea evitar tener logs puede comentar estas dos líneas
logging.basicConfig(level=logging.INFO) #
logger = logging.getLogger(__name__) #

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
    SYSTEM_PROMPT = """Eres un útil asistente de lectura que responde a preguntas 
    basándose en fragmentos de texto proporcionados en contexto. Responde sólo utilizando el contexto proporcionado, 
    siendo lo más conciso posible. Si no estás seguro, di que no lo sabes.
    Contexto:
    """

    # open file
    filename = file_Name
    paragraphs = parse_file(f"{filename}.txt")

    embeddings = get_embeddings(filename, embedding_model, paragraphs)

    conversation_history = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    while True:
        prompt = input(">>> Model " + ollama_model + ": ")
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
            stream=True  # Enable streaming
        )

        print("\n\n")
        for chunk in response:
            print(chunk["message"]["content"], end='', flush=True)

        # Add the assistant's response to the conversation history
        response_content = ''.join(chunk["message"]["content"] for chunk in response)
        conversation_history.append({"role": "assistant", "content": response_content})

if __name__ == "__main__":
    main()