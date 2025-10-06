import os
import chromadb
from chromadb import PersistentClient
import nltk
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer

# download once
# nltk.download("punkt")
# nltk.download("punkt_tab")

# Build a ChromaDB from the combined transcript file
def build_chroma_db(
    transcript_path: str,
    persist_dir: str = ".",        
    model_name: str = "all-MiniLM-L6-v2",
    batch_size: int = 5000,
):
    client = PersistentClient(path=persist_dir)
    collection = client.get_or_create_collection("love_is_blind")

    # chunk into setnences
    with open(transcript_path, "r", encoding="utf-8") as f:
        full_text = f.read()
    sentences = sent_tokenize(full_text)

    # embed all sentences 
    model = SentenceTransformer(model_name)
    embeddings = model.encode(sentences, show_progress_bar=True).tolist()

    # add to embeddings to ChromaDB
    ids = [f"sent_{i}" for i in range(len(sentences))]

    for i in range(0, len(sentences), batch_size):
        j = i + batch_size
        collection.add(
            ids=ids[i:j],
            documents=sentences[i:j],
            embeddings=embeddings[i:j],
        )
        print(f"  - Added items {i} through {j-1}")

    print(f"✅ Persisted {len(sentences)} sentences in batches of {batch_size}.")
    
if __name__ == "__main__":
    build_chroma_db("transcripts.txt")