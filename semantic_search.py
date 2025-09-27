from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_core.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain_openai import OpenAIEmbeddings

from qdrant_client.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

import os 
from dotenv import load_dotenv

load_dotenv()

# embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")


QDRANT_URL = os.getenv("QDRANT_URL") 
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")        
client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY, prefer_grpc=True)
vector_size = 3072  # Example vector size, adjust based on your embeddings
collection_name = "semantic_search_policy"


vector_store = QdrantVectorStore(
    client=client,
    collection_name="semantic_search_policy",
    embedding=embeddings,
)

# results = vector_store.similarity_search(
#     "What are the surrender charges when 3 premiums were paid?"
# )

query = input("Enter your query: ")
results = vector_store.similarity_search(query)
print(results[0])