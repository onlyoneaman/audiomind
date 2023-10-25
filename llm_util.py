import os
from util import get_env_var
import errno
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def initialize_llm():
    """Initialize the language model"""
    OPENAI_KEY = get_env_var("OPENAI_API_KEY")
    DREAMBOAT_KEY = os.getenv("DREAMBOAT_API_KEY")

    kwargs = {
        "temperature": 1,
        "model_name": "gpt-4", 
        "openai_api_key": OPENAI_KEY
    }
    if DREAMBOAT_KEY:
        kwargs.update({
            "openai_api_base": "https://dev.dreamboat.ai/v1/proxy",
            "headers": {
                "x-dreamboat-api-key": DREAMBOAT_KEY, 
                "x-dreamboat-mode": "proxy openai"
            }
        })
    return ChatOpenAI(**kwargs)

def load_transcript(transcript_file):
    if not os.path.exists(transcript_file):
        print("Error: Transcript file does not exist.")
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), transcript_file)
    return TextLoader(transcript_file).load()

def get_text_splitter():
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=6000, chunk_overlap=20, length_function=len)
    return text_splitter