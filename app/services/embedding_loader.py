from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import os

def load_and_chunk (filepath: str, 
                    chunk_size=500, 
                    chunk_overlap=100) -> list[Document]:
    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".pdf":
        loader = PyPDFLoader(filepath)
        raw_docs = loader.load()
    elif ext ==".txt":
        loader = TextLoader(filepath, encoding="utf-8")
        raw_docs = loader.load()
    else:
        raise ValueError(f"Unsupported file type: {ext}")
    
#   splitter = RecursiveCharacterTextSplitter.from_language(
#       language="en",
#       chunk_size=chunk_size
#       chunk_overlap=chunk_overlap 
#    )
    #not using from_language
    splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", "."," "],
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    chunks = splitter.split_documents(raw_docs)
    return chunks