from fastapi import FastAPI
from pydantic import BaseModel
from langfuse.langchain import CallbackHandler
from dotenv import load_dotenv
load_dotenv(".env")
langfuse_handler = CallbackHandler()
import requests
config  = {"configurable":{"thread_id":"2"},'callbacks':[langfuse_handler]}
from agent import create_agent
bot = create_agent()
app = FastAPI()
@app.post("/ask")
async def get_data(request:str):
    inputs = {"question":request}
    response = bot.invoke(inputs,config)
    final_messages = response['messages'][-1].content
    return  {"messages":final_messages}