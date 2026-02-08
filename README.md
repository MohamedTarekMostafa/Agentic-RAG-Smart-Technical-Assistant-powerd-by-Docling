# Agentic RAG: Smart Technical Assistant powerd by Docling
Logic : 
![WhatsApp Image 2026-02-07 at 9 47 14 PM](https://github.com/user-attachments/assets/8235c1b8-63f7-4a9a-aa85-fa7a0f630d78)

---

##  Overview
Welcome! This project is an **Agentic Retrieval-Augmented Generation (RAG)** system. Unlike a standard RAG that just looks at documents, this one acts like a "thinking" assistant. It evaluates your question first and decides whether it should check your local technical PDFs, search the live web, or just chat with you directly.

---

## How It Works
The system is built using a **Graph-based architecture** (LangGraph). Here’s the "brain" logic:

1.  **The Router:** When you ask a question, the AI determines the intent using a routing node.
2.  **Vector Store:** If you ask about technical ML details, it queries a ChromaDB index containing your specialized PDFs (processed via Docling).
3.  **Web Search:** If the information is too new or not in the documents, it uses Tavily to browse the live internet.
4.  **Direct Chat:** For greetings or general conversation, it responds instantly using its internal knowledge.
5.  **Memory:** It keeps track of your conversation history using a `thread_id`, so it remembers the context of your previous questions.

---

## The Tech Stack
* **LLM:** Llama 3.3 (70B) via Groq (for blazing fast inference).
* **Orchestration:** LangGraph (to manage the state and routing).
* **Document Parsing:** Docling (for high-fidelity Markdown conversion of PDFs).
* **Database:** ChromaDB (Vector storage).
* **Embeddings:** BAAI/bge-small-en-v1.5 (HuggingFace).
* **API:** FastAPI (Backend).
* **UI:** Streamlit (Frontend).

---

##  Getting Started

### 1. Setup Environment
Create a `.env` file in the root directory and add your keys:
```env
GROQ_API_KEY=your_groq_key
TAVILY_API_KEY=your_tavily_key
LANGFUSE_PUBLIC_KEY=your_optional_key
LANGFUSE_SECRET_KEY=your_optional_key
----
2. Prepare Documents
Place your PDF files (e.g., Machine_Learning_Design.pdf) in the project folder. The system will automatically parse them and create a local chroma_db folder on the first run.
3. Launch the Backend
python main.py
4. Launch the Frontend
Open a second terminal and run the Streamlit interface
streamlit run app.py
```
📁 Project Structure
tools.py: The "hands" of the agent (Web search and PDF retrieval logic).
nodes.py: The "logic steps" (Routing, Retrieving, and Generating).
agent.py: The "blueprint" that connects the nodes into a workflow graph.
main.py: The API layer (FastAPI) that hosts the agent and manages the session config.
app.py: The chat interface (Streamlit) that communicates with the API via REST.
Application Screenshots (Output)
![WhatsApp Image 2026-02-08 at 7 55 57 PM](https://github.com/user-attachments/assets/7fa7461c-c037-46ca-9ac9-d2c566232e9e)
![WhatsApp Image 2026-02-08 at 7 58 37 PM](https://github.com/user-attachments/assets/26054b99-2f40-43d3-8ed6-261af8ca85f6)
![WhatsApp Image 2026-02-08 at 7 59 42 PM](https://github.com/user-attachments/assets/d57a6e99-6ec9-4ab6-b723-9471436fe32d)
![WhatsApp Image 2026-02-08 at 8 00 50 PM](https://github.com/user-attachments/assets/2ebb8b99-f353-4f05-865e-b5c9b6b544fb)





