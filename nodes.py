from tools import web_search , retriever_tool 
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from typing import TypedDict
from typing_extensions import Annotated
from langgraph.graph import StateGraph,START,END,add_messages
load_dotenv(".env")
class State(TypedDict):
    messages : Annotated[list,add_messages]
    question  : str
    documents : str
    generation  :str
llm = ChatGroq(model = 'llama-3.3-70b-versatile',temperature = 0)
def web_search_node(state:State):
    print("WEB_SEARCH NODE Is Running.....")
    results = web_search(state['question'])
    if isinstance(results, str):
        return {"documents": results} 
    search_content = ""
    for res in results:
        if isinstance(res, dict) and 'content' in res:
            search_content += f"\nSource: {res.get('url', 'Unknown')}\nContent: {res['content']}\n"
        else:
            search_content += str(res) + "\n"    
    return {"documents": search_content}
def retriever_node(state: State):
    print("Retrieving from Vector Store.....")
    docs = retriever_tool(state['question']) 
    context = "\n".join([d.page_content for d in docs])
    return {"documents": context}

def generation_node(state:State):
    print("--- GENERATING ANSWER WITH MEMORY ---")
    question = state['question']
    History = state['messages']
    context = state.get("documents",'No Specefic Document Allowed')
    prompt = f""""You are a helpful AI assistant. Use the conversation history and the context below to answer
    Context: {context}
    History: {History}
    Question: {question}
    Answer:"""
    response = llm.invoke(prompt)
    return {"generation":response.content,"messages":[response]}
def router_node(state:State):
    print("Router_node is Running....")
    return state

def routing_decision(state):
    print("--- AI ROUTING ---")
    question = state["question"]
    
    router_prompt = f"""You are an expert router. 
    Your job is to decide the best source to answer the user's question.
    
    Rules:
    1. If the question is about technical topics found in a document (like AI papers, Machine Learning Books, specific technical details), use 'vectorstore'.
    2. If the question is a general greeting or small talk (like hi, hello, how are you), use 'direct'.
    3. If the question requires current events, news, or general knowledge NOT in a specific document, use 'web_search'.

    Question: {question}
    Answer only with one word: 'vectorstore', 'web_search', or 'direct'. No explanation."""

    response = llm.invoke(router_prompt)
    decision = response.content.strip().lower()

    if "vectorstore" in decision:
        return "vectorstore"
    elif "direct" in decision:
        return "direct"
    else:
        return "web_search"
