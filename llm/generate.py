import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from llm.prompts import build_prompt
load_dotenv()
QDRANT_URL = os.getenv("QDRANT_URL") or st.secrets["QDRANT_URL"]
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY") or st.secrets["QDRANT_API_KEY"]
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY") or st.secrets["NVIDIA_API_KEY"]

if not NVIDIA_API_KEY:
    raise ValueError("NVIDIA_API_KEY is missing from .env")


client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=NVIDIA_API_KEY
)


MODEL_NAME = "nvidia/nemotron-3-ultra-550b-a55b"
# MODEL_NAME = "openai/gpt-oss-20b"
def generate_answer(query, results):

    system_prompt, user_prompt = build_prompt(query, results)
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0.3,
        max_tokens=1800
    )
    return response.choices[0].message.content