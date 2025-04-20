from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import os

def load_and_chunk (filepath: str, 
                    chunk_size=500, 
                    chunk_overlap=100) -> list[Document]: # prepare the file into a sizeable format for embedding
    ext = os.path.splitext(filepath)[1].lower() #the ending, the file type

    if ext == ".pdf":
        loader = PyPDFLoader(filepath)
        raw_docs = loader.load()
    elif ext ==".txt":
        loader = TextLoader(filepath, encoding="utf-8")
        raw_docs = loader.load()
    else:
        raise ValueError(f"Unsupported file type: {ext}") # fall back system
    
#   splitter = RecursiveCharacterTextSplitter.from_language(
#       language="en",
#       chunk_size=chunk_size
#       chunk_overlap=chunk_overlap 
#    )
    #not using from_language
    splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", "."," "], # self declaring seperator
        chunk_size=chunk_size, # how big should each chunk be in case that the separators fail
        chunk_overlap=chunk_overlap # how much should they overlap each other to retain coherrency
    )

    chunks = splitter.split_documents(raw_docs) # .split_documents() comes from LangChain's RecursiveCharacterTextSplitter class.
    return chunks