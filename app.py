import streamlit as st
import requests

# --- Page Config ---
st.set_page_config(page_title="Agentic RAG", layout="centered")
st.title("🤖 Agentic RAG with Docling")
st.info("Ask questions about Machine Learning (Docs) or Current Events (Web).")

# --- Backend Configuration ---
# Ensure your FastAPI server (main.py) is running on this URL
BACKEND_URL = "http://127.0.0.1:550/ask"

# Initialize Session Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Main Interaction ---
if prompt := st.chat_input("What would you like to know?"):
    # 1. Add and display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Send request to FastAPI backend
    with st.chat_message("assistant"):
        with st.spinner("Agent is thinking..."):
            try:
                # Note: In your FastAPI code, you used 'request:str' as a query parameter
                # So we pass it as a parameter in the URL
                response = requests.post(
                    BACKEND_URL, 
                    params={"request": prompt}  # Matches 'request:str' in your @app.post
                )
                
                if response.status_code == 200:
                    # Extract final message from your FastAPI return {"messages": final_messages}
                    api_data = response.json()
                    answer = api_data.get("messages", "No response received.")
                    
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error(f"Backend Error: {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                st.error("Failed to connect to the backend. Is main.py running?")

# --- Sidebar ---
with st.sidebar:
    st.header("Project Info")
    st.write("This UI communicates with the FastAPI backend using REST.")
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()