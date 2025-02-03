![](https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/DeepSeek_logo.svg/1280px-DeepSeek_logo.svg.png)

# DeepSeek Web Researcher

DeepSeek Web Researcher is an advanced research assistant tool designed to automate and streamline the process of gathering and summarizing information from the web. Inspired by the [LangChain Ollama Deep Researcher](https://github.com/langchain-ai/ollama-deep-researcher), this project enhances research workflows by leveraging Deepseek R1 preview model on Groq l and Tavily's web search API. The tool iteratively searches, summarizes, and refines information to deliver comprehensive, well-structured research outputs.

## Features

- 🔍 **Automated Web Research**: Utilizes Tavily API for targeted web searches.
- 🧐 **AI-Powered Summarization**: Employs Groq's DeepSeek R1 model to summarize and synthesize research findings.
- 🔄 **Iterative Research Loops**: Identifies knowledge gaps and refines search queries to ensure thorough coverage.
- 📅 **User-Friendly Interface**: Streamlit-based UI for seamless interaction.


## Inspiration

This project draws inspiration from the [LangChain Ollama Deep Researcher](https://github.com/langchain-ai/ollama-deep-researcher), adopting its modular approach to automating deep research tasks. By integrating LangChain's robust framework with models served by Groq and Tavily's efficient search capabilities, DeepSeek Web Researcher offers a more scalable and powerful solution.

## Demo

Here are two demo results for a couple of questions:

![](https://github.com/yYorky/DeepSeek-Researcher/blob/main/DeepResearch_1.gif?raw=true)



![](https://github.com/yYorky/DeepSeek-Researcher/blob/main/DeepResearch_2.gif?raw=true)



## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yYorky/DeepSeek-Researcher.git
   cd deepseek-researcher
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   conda activate venv
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root directory and add your API keys:

   ```env
   GROQ_API_KEY=your_groq_api_key
   TAVILY_API_KEY=your_tavily_api_key
   ```

## Usage

1. **Run the application:**

   ```bash
   streamlit run app.py
   ```

2. **Enter a research topic** in the input field and click "Start Research".

3. **Review the results**, including the research summary, identified knowledge gaps, and sources.

## Project Structure

- `app.py`: Main application file running the Streamlit interface.
- `configuration.py`: Configurations for model selection and API usage.
- `utils.py`: Utility functions for API calls and formatting.
- `state.py`: Defines the data structures for managing research states.
- `graph.py`: Core logic handling the research process flow.
- `prompts.py`: Templates for query generation, summarization, and reflection prompts.
- `requirements.txt`: Lists all Python dependencies.

## Technologies Used

- **[LangChain](https://github.com/langchain-ai/langchain)**: Framework for developing applications powered by language models.
- **DeepSeek R1 Model**: Reasoning model for natural language processing.
- **[Tavily](https://www.tavily.com/)**: Web search API for fetching real-time information.
- **[Streamlit](https://streamlit.io/)**: Framework for building interactive web apps with Python.

## Acknowledgments

Special thanks to the [LangChain](https://github.com/langchain-ai/langchain) team for their pioneering work on the Ollama Deep Researcher, which served as the foundation for this project.

