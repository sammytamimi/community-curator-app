import argparse
import os
import sys

# This MUST be before any local imports to fix the ModuleNotFoundError
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from dotenv import load_dotenv
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from core.loader import get_document_chunks_from_pdf

# Load environment variables from .env file
load_dotenv()

# Define the persistent directory for ChromaDB
CHROMA_DB_DIR = os.path.join(os.path.dirname(__file__), '..', 'vector_db')
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')


def main(file_name: str):
    """
    Main function to orchestrate the PDF ingestion process.
    """
    print("--- Starting PDF Ingestion Process ---")

    # 1. Initialize the Azure OpenAI Embeddings model
    print("Initializing Azure OpenAI Embeddings model...")
    try:
        embeddings = AzureOpenAIEmbeddings(
            azure_deployment=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_ID"),
            chunk_size=1,  # Recommended for Azure OpenAI
        )
        print("Embeddings model initialized successfully.")
    except Exception as e:
        print(f"Error initializing embeddings model: {e}")
        return

    # 2. Load and process document chunks from the PDF file
    file_path = os.path.join(DATA_DIR, file_name)
    chunks = get_document_chunks_from_pdf(file_path)

    if not chunks:
        print("No document chunks were created. Halting ingestion process.")
        return

    # 3. Initialize ChromaDB and add documents
    print(f"Initializing ChromaDB at: {CHROMA_DB_DIR}")
    try:
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=CHROMA_DB_DIR
        )
        print("Persisting vectors to ChromaDB...")
        vector_store.persist()
        print(f"Successfully added {len(chunks)} document chunks to the vector store.")
    except Exception as e:
        print(f"Error creating or adding to ChromaDB vector store: {e}")
        return

    print("--- PDF Ingestion Process Complete ---")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Ingest data from a PDF file into a ChromaDB vector store."
    )
    parser.add_argument(
        "file_name",
        type=str,
        help="The name of the PDF file located in the 'backend/data' directory."
    )
    args = parser.parse_args()

    main(args.file_name) 