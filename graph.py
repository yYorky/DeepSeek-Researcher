import os
import json
from typing_extensions import Literal
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langchain_groq import ChatGroq
from langgraph.graph import START, END, StateGraph
from configuration import Configuration, SearchAPI
from utils import tavily_search, format_sources
from state import SummaryState, SummaryStateInput, SummaryStateOutput
from prompts import query_writer_instructions, summarizer_instructions, reflection_instructions
import streamlit as st
import re

from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Fetch API Key from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("Missing GROQ API key. Please set it in a .env file.")

# Initialize the Groq LLM model
llm_groq = ChatGroq(model="llama-guard-3-8b", api_key=GROQ_API_KEY)

def extract_json(text):
    """ Extract JSON from the response text """
    match = re.search(r"\{.*\}", text, re.DOTALL)  # Extract first JSON-like content
    if match:
        return match.group(0)
    return None

def generate_query(state, config):
    """ Generate a query for web search """
    
    # Format the prompt
    query_writer_instructions_formatted = query_writer_instructions.format(research_topic=state.research_topic)

    # Call the LLM
    result = llm_groq.invoke([
        SystemMessage(content=query_writer_instructions_formatted),
        HumanMessage(content="Generate a query for web search:")
    ])
    
    # # Debug: Print the LLM response
    # st.write("DEBUG: LLM Response Content", result.content)  

    # Extract only the JSON part
    extracted_json = extract_json(result.content)

    if not extracted_json:
        st.error("Failed to extract valid JSON from LLM response.")
        return {"search_query": "default search query"}  # Fallback

    # Ensure the response is valid JSON
    try:
        query = json.loads(extracted_json)
    except json.JSONDecodeError as e:
        st.error(f"Error decoding JSON: {e}")
        return {"search_query": "default search query"}  # Fallback query

    if "query" not in query:
        st.error("Invalid response format from LLM. Expected JSON with 'query' key.")
        return {"search_query": "default search query"}

    return {"search_query": query['query']}

def web_research(state: SummaryState, config: RunnableConfig):
    """ Gather information from the web """
    configurable = Configuration.from_runnable_config(config)
    search_results = tavily_search(state.search_query, include_raw_content=True, max_results=1)
    return {
        "sources_gathered": [format_sources(search_results)], 
        "research_loop_count": state.research_loop_count + 1,
        "web_research_results": [search_results]
    }

def summarize_sources(state: SummaryState, config: RunnableConfig):
    """ Summarize the gathered sources """
    human_message_content = (
        f"Generate a summary of these search results: {state.web_research_results[-1]} "
        f"That addresses the following topic: {state.research_topic}"
    )
    result = llm_groq.invoke(
        [SystemMessage(content=summarizer_instructions),
        HumanMessage(content=human_message_content)]
    )
    return {"running_summary": result.content}

def reflect_on_summary(state, config):
    """ Reflect on the summary and generate a follow-up query """

    # LLM Reflection Prompt
    result = llm_groq.invoke([
        SystemMessage(content=reflection_instructions.format(research_topic=state.research_topic)),
        HumanMessage(content=f"Identify a knowledge gap and generate a follow-up web search query: {state.running_summary}")
    ])
    
    # # Debugging: Print Raw Response
    # st.write("DEBUG: LLM Reflection Response", result.content)

    # Extract JSON from Response
    extracted_json = extract_json(result.content)

    if not extracted_json:
        st.error("Failed to extract valid JSON from LLM response.")
        return {"search_query": f"Tell me more about {state.research_topic}"}  # Fallback

    # Parse Extracted JSON
    try:
        follow_up_query = json.loads(extracted_json)
    except json.JSONDecodeError as e:
        st.error(f"Error decoding JSON: {e}")
        return {"search_query": f"Tell me more about {state.research_topic}"}  # Fallback query

    # Ensure query exists in response
    if "follow_up_query" not in follow_up_query:
        st.error("Invalid response format. Expected 'follow_up_query' key.")
        return {"search_query": f"Tell me more about {state.research_topic}"}

    return {"search_query": follow_up_query['follow_up_query']}

def finalize_summary(state: SummaryState):
    """ Finalize the summary """
    all_sources = "\n".join(state.sources_gathered)
    state.running_summary = f"## Summary\n\n{state.running_summary}\n\n### Sources:\n{all_sources}"
    return {"running_summary": state.running_summary}

# Add nodes and edges 
builder = StateGraph(SummaryState, input=SummaryStateInput, output=SummaryStateOutput, config_schema=Configuration)
builder.add_node("generate_query", generate_query)
builder.add_node("web_research", web_research)
builder.add_node("summarize_sources", summarize_sources)
builder.add_node("reflect_on_summary", reflect_on_summary)
builder.add_node("finalize_summary", finalize_summary)

builder.add_edge(START, "generate_query")
builder.add_edge("generate_query", "web_research")
builder.add_edge("web_research", "summarize_sources")
builder.add_edge("summarize_sources", "reflect_on_summary")
builder.add_conditional_edges("reflect_on_summary", lambda state, config: "web_research" if state.research_loop_count <= 3 else "finalize_summary")
builder.add_edge("finalize_summary", END)

graph = builder.compile()