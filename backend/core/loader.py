import pandas as pd
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List


def get_document_chunks_from_excel(file_path: str, url_column_name: str) -> List:
    """
    Loads URLs from a specified column in an Excel file, scrapes their content,
    and splits the content into manageable document chunks.

    Args:
        file_path: The path to the Excel file.
        url_column_name: The name of the column containing the URLs.

    Returns:
        A list of document chunks.
    """
    print(f"Reading URLs from {file_path}...")
    try:
        df = pd.read_excel(file_path)
        if url_column_name not in df.columns:
            raise ValueError(
                f"Column '{url_column_name}' not found in Excel file at {file_path}"
            )
        urls = df[url_column_name].dropna().tolist()
        if not urls:
            print("No URLs found in the specified column.")

            return []
        print(f"Found {len(urls)} URLs to process.")
    except Exception as e:
        print(f"Error reading or processing Excel file: {e}")
        return []

    # Using continue_on_failure=True to ensure the process doesn't stop for a single bad URL.
    loader = UnstructuredURLLoader(urls=urls, continue_on_failure=True)

    print("Loading and scraping content from URLs... This may take a few moments.")
    documents = loader.load()

    if not documents:
        print("Could not load any content from the provided URLs.")
        return []

    print(f"Successfully loaded content from {len(documents)} URLs.")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split the content into {len(chunks)} searchable chunks.")

    return chunks

