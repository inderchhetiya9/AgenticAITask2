import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, AzureOpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
load_dotenv()
# Toggle this for Azure vs Standard OpenAI
# embedding_model = AzureOpenAIEmbeddings(...) 
embedding_model = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))

VECTOR_STORE_PATH = "faiss_index"

def ingest_documents(file_paths):
    """
    Task 2: Convert docs to embeddings and store in FAISS.
    """
    documents = []
    for path in file_paths:
        if path.endswith(".pdf"):
            loader = PyPDFLoader(path)
        else:
            loader = TextLoader(path)
        documents.extend(loader.load())

    # Split text into chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)

    # Create/Update Vector Store
    vector_store = FAISS.from_documents(docs, embedding_model)
    vector_store.save_local(VECTOR_STORE_PATH)
    print(f"Stored {len(docs)} chunks in FAISS.")

def get_retriever():
    """
    Returns the vector store as a retriever for the Agent.
    """
    if os.path.exists(VECTOR_STORE_PATH):
        vector_store = FAISS.load_local(VECTOR_STORE_PATH, embedding_model, allow_dangerous_deserialization=True)
        return vector_store.as_retriever(search_kwargs={"k": 3})
    else:
        raise ValueError("Vector store not found. Please ingest documents first.")