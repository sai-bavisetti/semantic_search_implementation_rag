from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant

from qdrant_client.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

import os 
from dotenv import load_dotenv


load_dotenv()

file_path = "policy.pdf"
loader = PyPDFLoader(file_path)

docs = loader.load()

# print(len(docs))
# print(f"{docs[0].page_content[:100]}\n")
# print(docs[0].metadata)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True
)
all_splits = text_splitter.split_documents(docs)

print(len(all_splits))

# # Google Embeddings
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

# # HuggingFace Embeddings
# embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# OpenAI Embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")


vector_1 = embeddings.embed_query(all_splits[0].page_content)
vector_2 = embeddings.embed_query(all_splits[1].page_content)

assert len(vector_1) == len(vector_2)
print(f"Generated vectors of length {len(vector_1)}\n")
print(vector_1[:10])


QDRANT_URL = os.getenv("QDRANT_URL") 
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY") 

client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
vector_size = len(vector_1)

if not client.collection_exists("semantic_search_policy"):
    client.create_collection(
        collection_name="semantic_search_policy",
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
    )
vector_store = QdrantVectorStore(
    client=client,
    collection_name="semantic_search_policy",
    embedding=embeddings,
)

ids = vector_store.add_documents(documents=all_splits)

results = vector_store.similarity_search(
    "What are the surrender charges when 3 premiums were paid?"
)