import os
from openai import OpenAI
from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer

os.environ["TOKENIZERS_PARALLELISM"] = "false"

client = OpenAI(
  api_key='{enter your own API key here}'
)

# open ChromaDB client
vectordb   = PersistentClient(path=".")
collection = vectordb.get_or_create_collection("love_is_blind")

# load Hugging Face embedder
model = SentenceTransformer("all-MiniLM-L6-v2")

#retriever
def retrieve_context(
    user_query: str,
    top_k: int = 5
):
    # embed the user query
    q_emb = model.encode([user_query], show_progress_bar=False)[0]

    # query Chroma for nearest neighbors
    results = collection.query(
        query_embeddings=[q_emb],
        n_results=top_k,
    )
    return results["documents"][0]

# generator
def rag_completion(user_prompt: str):

    context_sentences = retrieve_context(user_prompt)
    context_sentences = "\n".join(f"- {s}" for s in context_sentences)

    augmented = (
        "Here are some relevant transcript snippets from real life situations for tone and context. Use these to aid your answer:\n"
        f"{context_sentences}\n\n"
        "Now, using that style, please write three flirty responses the user could send in this situation.\n"
        f"Keep it short. Don't be scared to be a little cheeky:\n\n{user_prompt}."
        )
        

    print("\n--- FULL PROMPT SENT TO MODEL ---")
    print(augmented)

    # minor prompt engineering
    chat_resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": ("You are a charming, witty, and emotionally intelligent flirting assistant. "
            "Your job is to help the user craft smooth, confident, and flirtatious messages for a romantic interest. "
            "Your responses should feel natural, playful, and human — like something a charismatic friend would say. "
            "Draw inspiration from the style, tone, and phrasing of the provided transcript snippets, mimicking their emotional flow and conversational rhythm. "
            "Keep things light, warm, short, and a little bold.")},
            {"role": "user",   "content": augmented}
        ],
        temperature=0.8,
    )
    return chat_resp.choices[0].message.content

if __name__ == "__main__":
    prompt = input("Need help flirting? Give me the scenario and I'll drop some lines for you to choose from.\n")
    answer = rag_completion(prompt)
    print("\n--- RAG ANSWER ---")
    print(answer)