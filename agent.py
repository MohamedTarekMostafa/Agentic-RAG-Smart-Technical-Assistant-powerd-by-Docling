from nodes import router_node,retriever_node,web_search_node,generation_node,State,routing_decision
from langgraph.graph import END, StateGraph,START
from langgraph.checkpoint.memory import MemorySaver 
from IPython.display import Image, display
from dotenv import load_dotenv
load_dotenv(".env")
def create_agent():
    workflow = StateGraph(State)
    checkpoint_memory = MemorySaver() 
    workflow = StateGraph(State)
    workflow.add_node("router_node", router_node)
    workflow.add_node("retriever", retriever_node)
    workflow.add_node("web_search", web_search_node)
    workflow.add_node("generate", generation_node)
    workflow.add_edge(START, 'router_node')

    workflow.add_conditional_edges(
    'router_node',
    routing_decision,
    {
        "vectorstore": "retriever",
        "web_search": "web_search",
        "direct": "generate",
    },
)
    workflow.add_edge("web_search", "generate")
    workflow.add_edge("retriever", "generate")
    workflow.add_edge("generate", END)

    return  workflow.compile(checkpointer=checkpoint_memory)
