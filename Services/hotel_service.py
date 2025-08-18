# hotel_rag_agent.py         # Main RAG + Gemini logic
# hotel_preferences.txt      # Raw user preference text
# chroma_persistent_storage/ # ChromaDB index (auto-created)


import os
import json
from dotenv import load_dotenv
import chromadb
from chromadb.utils import embedding_functions
import google.generativeai as genai

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Gemini model setup
generation_config = genai.GenerationConfig(
    temperature=0.4,
    max_output_tokens=800,
    top_p=1,
    top_k=1
)
gemini_model = genai.GenerativeModel("gemini-1.5-flash", generation_config=generation_config)

# ChromaDB setup
chroma_client = chromadb.PersistentClient(path="chroma_persistent_storage")
collection = chroma_client.get_or_create_collection(
    name="hotel_pref_collection",
    embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
)

# Load and chunk hotel preference text
def load_and_index_preferences(filename="hotel_preferences.txt"):
    with open(filename, "r", encoding="utf-8") as f:
        text = f.read()

    chunks = [text[i:i+500] for i in range(0, len(text), 480)]
    for i, chunk in enumerate(chunks):
        collection.upsert(
            ids=[f"pref_chunk_{i+1}"],
            documents=[chunk]
        )
    print(f"Indexed {len(chunks)} chunks from {filename}")

# Query ChromaDB
def retrieve_context(query="hotel preferences"):
    results = collection.query(query_texts=[query], n_results=3)
    chunks = [doc for sublist in results["documents"] for doc in sublist]
    return "\n".join(chunks)

# Generate structured hotel preference JSON
def generate_hotel_preferences(context):
    prompt = f"""
        You are an AI assistant that extracts hotel preferences from user context.

        Context:
        {context}

        Respond with a JSON object containing:
        - location
        - stay_dates
        - hotel_preferences:
            - rating
            - amenities
            - price_range

        If any field is missing, set it to null.
        IMPORTANT: Return ONLY the JSON object. No markdown or extra text.
        """

    response = gemini_model.generate_content(prompt)
    response_text = response.text.strip()

    if response_text.startswith("```"):
        response_text = response_text.replace("```json", "").replace("```", "").strip()

    try:
        parsed = json.loads(response_text)
        return {"status": "success", "data": parsed}
    except json.JSONDecodeError:
        return {"status": "success", "data": response_text}
