import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from langchain_community.chat_models import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
from ..prompts import SUMMARY_PROMPT, TIMELINE_PROMPT
import os

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", openai_api_key=os.environ.get("OPENAI_API_KEY"))

def summarize_chunks(x):
    chain = load_summarize_chain(llm, chain_type="map_reduce", map_prompt=SUMMARY_PROMPT)
    return {"summary": chain.run(x["chunks"])}

def summarize_timeline(x):
    chain = load_summarize_chain(llm, chain_type="stuff", prompt=TIMELINE_PROMPT)
    return {"timeline": chain.run(x["chunks"][0])}  # Simplified to one chunk
