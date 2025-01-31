import streamlit as st
from state import SummaryState
from graph import graph
import os
from dotenv import load_dotenv

load_dotenv()

tavily_api_key = os.getenv("TAVILY_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

if not tavily_api_key or not groq_api_key:
    raise ValueError("Missing API keys. Please set them in a .env file.")


# Set page title and layout
st.set_page_config(page_title="DeepSeek Web Researcher")

# App Header
st.title("🔍 DeepSeek Web Researcher")

# User Input for Research Topic
research_topic = st.text_input("Enter a research topic:", placeholder="e.g. Manchester United tactics")

if st.button("Start Research"):
    if research_topic:
        with st.spinner("🧐 Researching... This may take a moment."):
            state = SummaryState(research_topic=research_topic)
            final_result = graph.invoke(state)

        # Extract components from the final result
        research_summary = final_result["running_summary"]

        # Display Research Summary
        st.subheader("📌 Research Summary")
        st.markdown(research_summary)

        # Extract and display structured insights
        with st.expander("🤖 DeepSeek Model's Thought Process"):
            st.markdown("### DeepSeek's Internal Reasoning")
            deepseek_thoughts = research_summary.split("</think>")[0] + "</think>" if "<think>" in research_summary else "No explicit thought process found."
            st.info(deepseek_thoughts)

        # Display Follow-Up Reflections (if available)
        if "knowledge_gap" in final_result and "follow_up_query" in final_result:
            st.subheader("🔄 Research Refinements")
            st.write(f"**Identified Knowledge Gap:** {final_result['knowledge_gap']}")
            st.write(f"**Next Research Query:** {final_result['follow_up_query']}")

        # Display Sources in a Neat Format
        if "sources_gathered" in final_result:
            st.subheader("📚 Research Sources")
            for source in final_result["sources_gathered"]:
                st.markdown(f"🔗 [{source.split(': ')[-1]}]({source.split(': ')[-1]})")

    else:
        st.warning("⚠️ Please enter a research topic before starting.")
