from docling.document_converter import DocumentConverter
import re
from langchain_core.documents import Document as LangchainDocument
from langchain_tavily import TavilySearch
from langchain.tools import tool
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter 
embeddings = HuggingFaceEmbeddings(model_name = 'BAAI/bge-small-en-v1.5')
import os
load_dotenv(".env")
file_list = ['Machine_Learning_Design.pdf','Luis_Serrano_Grokking_Machine_Learning_2021,_Manning_Publications.pdf']
search_tool = TavilySearch(max_results=3)
def web_search(query):
    return search_tool.run(query)
def retriever_tool(question):
    
    persist_dir = "./chroma_db"
    if os.path.exists(persist_dir):
        vector_store = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
    else:
        converter = DocumentConverter()
        all_chunks = []

        for file_path in file_list:
           result = converter.convert(file_path)
           md_text = result.document.export_to_markdown()
           sections = re.split(r'\n#{1,3} ', md_text)
           for section in sections:
              section = section.strip()
              if len(section) < 100:
                  continue

              all_chunks.append(
                LangchainDocument(
                    page_content=section,
                    metadata={"source": file_path} 
                )
            )        

        vector_store = Chroma.from_documents(documents=all_chunks, embedding=embeddings, persist_directory=persist_dir)
    
    retriever_obj = vector_store.as_retriever(search_kwargs={"k": 3})
    results = retriever_obj.invoke(question)
    return results
