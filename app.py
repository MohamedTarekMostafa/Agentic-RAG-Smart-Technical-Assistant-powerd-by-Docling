import streamlit as st
import requests

st.set_page_config(page_title="Agentic RAG", layout="centered")
st.title("🤖 Agentic RAG with Docling")
st.info("Ask questions about Machine Learning (Docs) or Current Events (Web).")

BACKEND_URL = "http://127.0.0.1:550/ask"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What would you like to know?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Agent is thinking..."):
            try:
                response = requests.post(
                    BACKEND_URL, 
                    params={"request": prompt}  
                )
                
                if response.status_code == 200:
                    api_data = response.json()
                    answer = api_data.get("messages", "No response received.")
                    
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error(f"Backend Error: {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                st.error("Failed to connect to the backend. Is main.py running?")

with st.sidebar:
    st.header("Project Info")
    st.write("This UI communicates with the FastAPI backend using REST.")
    if st.button("Clear Chat"):
        st.session_state.messages = []

        st.rerun()
