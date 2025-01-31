import os
import requests
from typing import Dict, Any
from langsmith import traceable
from tavily import TavilyClient
from langchain_groq import ChatGroq

from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Fetch API Key from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("Missing GROQ API key. Please set it in a .env file.")

# Initialize the Groq LLM model
llm_groq = ChatGroq(model="deepseek-r1-distill-llama-70b", api_key=GROQ_API_KEY)

@traceable
def groq_search(query: str) -> Dict[str, Any]:
    """ Use Groq's LLaMA model to generate a response. """
    response = llm_groq.invoke(query)
    return {"results": [{"title": "Groq LLM Response", "url": "N/A", "content": response.content}]}

def format_sources(search_results):
    """Format search results into a bullet-point list of sources."""
    return '\n'.join(
        f"* {source['title']} : {source['url']}"
        for source in search_results['results']
    )

@traceable
def tavily_search(query, include_raw_content=True, max_results=3):
    """ Search the web using Tavily API. """
    tavily_client = TavilyClient()
    return tavily_client.search(query, 
                         max_results=max_results, 
                         include_raw_content=include_raw_content)
