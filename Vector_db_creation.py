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
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('vector_db_creation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


load_dotenv()
logger.info("Environment variables loaded successfully")

file_path = "policy.pdf"
logger.info(f"Loading PDF document from: {file_path}")
loader = PyPDFLoader(file_path)

docs = loader.load()
logger.info(f"Successfully loaded {len(docs)} pages from PDF")

# print(len(docs))
# print(f"{docs[0].page_content[:100]}\n")
# print(docs[0].metadata)

logger.info("Initializing text splitter with chunk_size=1000, chunk_overlap=200")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True
)
all_splits = text_splitter.split_documents(docs)
logger.info(f"Document split into {len(all_splits)} chunks")

# print(len(all_splits))

# # Google Embeddings
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

# # HuggingFace Embeddings
# embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# OpenAI Embeddings
logger.info("Initializing OpenAI embeddings with model: text-embedding-3-large")
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

logger.info("Generating test embeddings for first two document chunks")
vector_1 = embeddings.embed_query(all_splits[0].page_content)
vector_2 = embeddings.embed_query(all_splits[1].page_content)

assert len(vector_1) == len(vector_2)
logger.info(f"Generated vectors of length {len(vector_1)}")
print(f"Generated vectors of length {len(vector_1)}\n")
print(vector_1[:10])


QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

logger.info(f"Connecting to Qdrant at URL: {QDRANT_URL}")
client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
vector_size = len(vector_1)
logger.info(f"Using vector size: {vector_size}")

if not client.collection_exists("semantic_search_policy"):
    logger.info("Creating new Qdrant collection: semantic_search_policy")
    client.create_collection(
        collection_name="semantic_search_policy",
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
    )
    logger.info("Collection created successfully")
else:
    logger.info("Collection 'semantic_search_policy' already exists")

logger.info("Initializing QdrantVectorStore")
vector_store = QdrantVectorStore(
    client=client,
    collection_name="semantic_search_policy",
    embedding=embeddings,
)

logger.info(f"Adding {len(all_splits)} documents to vector store")
ids = vector_store.add_documents(documents=all_splits)
logger.info(f"Successfully added documents with IDs: {ids[:5]}..." if len(ids) > 5 else f"Successfully added documents with IDs: {ids}")

logger.info("Testing similarity search with sample query")
results = vector_store.similarity_search(
    "What are the surrender charges when 3 premiums were paid?"
)
logger.info(f"Similarity search returned {len(results)} results")