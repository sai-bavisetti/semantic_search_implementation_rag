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
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('semantic_search.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

load_dotenv()
logger.info("Environment variables loaded successfully")

# embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
logger.info("Initializing OpenAI embeddings with model: text-embedding-3-large")
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
logger.info(f"Connecting to Qdrant at URL: {QDRANT_URL}")
client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY, prefer_grpc=True)
vector_size = 3072  # Example vector size, adjust based on your embeddings
collection_name = "semantic_search_policy"
logger.info(f"Using collection: {collection_name} with vector size: {vector_size}")


logger.info("Initializing QdrantVectorStore for semantic search")
vector_store = QdrantVectorStore(
    client=client,
    collection_name="semantic_search_policy",
    embedding=embeddings,
)

# results = vector_store.similarity_search(
#     "What are the surrender charges when 3 premiums were paid?"
# )

query = input("Enter your query: ")
logger.info(f"User query received: {query}")
logger.info("Performing similarity search...")
results = vector_store.similarity_search(query)
logger.info(f"Search completed. Found {len(results)} results")
logger.info("Displaying top result:")
print(results[0])