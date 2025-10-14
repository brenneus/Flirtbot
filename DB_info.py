# This was used as a testing file 

import nltk
from nltk.tokenize import sent_tokenize

with open("transcripts.txt", "r", encoding="utf-8") as f:
    text = f.read()

sentences = sent_tokenize(text)
print(f"Found {len(sentences)} sentences in transcript.txt")

# inspect_db.py
from chromadb import PersistentClient

db = PersistentClient(path=".")
col = db.get_or_create_collection("love_is_blind")

# fetch *all* stored docs
res = col.get(include=["documents"], limit=15_000)
print(f"Chroma holds {len(res['documents'])} documents")