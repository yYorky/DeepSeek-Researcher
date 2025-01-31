import os
import json
import re
import streamlit as st
from state import SummaryState
from graph import graph
from dotenv import load_dotenv

load_dotenv()

tavily_api_key = os.getenv("TAVILY_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

if not tavily_api_key or not groq_api_key:
    raise ValueError("Missing API keys. Please set them in a .env file.")

# Set page title and layout
st.set_page_config(page_title="DeepSeek Web Researcher", layout="wide")

# App Header
st.title("🔍 DeepSeek Web Researcher")

# User Input for Research Topic
research_topic = st.text_input("Enter a research topic:", placeholder="e.g. Manchester United tactics")

def extract_thought_process(text):
    """Extract the <think> section from the LLM response."""
    match = re.search(r"<think>(.*?)</think>", text, re.DOTALL)
    return match.group(1).strip() if match else None

def extract_json(text):
    """ Extract JSON from the response text """
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            return None
    return None

if st.button("Start Research"):
    if research_topic:
        col1, col2 = st.columns([1, 1])  # Create two columns for layout
        with col2:
            st.subheader("🔄 Research in Progress")
            progress_placeholder = st.empty()

        with st.spinner("🧐 Researching... This may take a moment."):
            state = SummaryState(research_topic=research_topic)
            final_result = graph.invoke(state)

        # Extract Research Summary
        research_summary = final_result.get("running_summary", "No summary generated.")

        # Extract Thought Process
        thought_process = extract_thought_process(research_summary)
        research_summary_cleaned = re.sub(r"<think>.*?</think>", "", research_summary, flags=re.DOTALL).strip()

        # Display Research Summary in left column
        with col1:
            st.subheader("📌 Research Summary")
            st.markdown(research_summary_cleaned)

        # Display Thought Process in right column during and after processing
        with col2:
            if thought_process:
                st.subheader("🤖 DeepSeek Model's Thought Process")
                st.info(thought_process)
            else:
                progress_placeholder.text("Processing insights... Generating thought process...")

        # Display Follow-Up Reflections (if available)
        if "knowledge_gap" in final_result and "follow_up_query" in final_result:
            with col1:
                st.subheader("🔄 Research Refinements")
                st.write(f"**Identified Knowledge Gap:** {final_result['knowledge_gap']}")
                st.write(f"**Next Research Query:** {final_result['follow_up_query']}")

        # Display Sources in a structured format
        if "sources_gathered" in final_result:
            with col1:
                st.subheader("📚 Research Sources")
                for source in final_result["sources_gathered"]:
                    st.markdown(f"🔗 [{source.split(': ')[-1]}]({source.split(': ')[-1]})")
    else:
        st.warning("⚠️ Please enter a research topic before starting.")
