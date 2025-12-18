#read the files
#split into chunks
#generate embeddings
#store in vector store -- FAISS

import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

#load environment variables from .env file
load_dotenv(dotenv_path='../.env')
DATA_PATH="../knowledge_base"
FAISS_INDEX_PATH="../faiss_index"

print("Loading and processing documents...")

# Load documents from the specified directory
txt_loader = DirectoryLoader(DATA_PATH, glob="**/*.txt", loader_cls=TextLoader,
loader_kwargs={"encoding": "utf8"}) 
txt_docs = txt_loader.load()

pdf_loader = DirectoryLoader(DATA_PATH, glob="**/*.pdf", loader_cls=PyPDFLoader,)
pdf_docs = pdf_loader.load()

docs = txt_docs + pdf_docs

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

docs = text_splitter.split_documents(docs)

print("Generating embeddings...")

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

db = FAISS.from_documents(docs, embeddings)

db.save_local(FAISS_INDEX_PATH)

print("FAISS index created and saved successfully.")