import os
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode

# Load API key from environment or Streamlit secrets
def get_tavily_api_key():
    # Try environment variable first
    api_key = os.getenv("TAVILY_API_KEY")
    if api_key:
        return api_key
    # Try Streamlit secrets (for cloud deployment)
    try:
        import streamlit as st
        return st.secrets.get("TAVILY_API_KEY")
    except:
        return None

def get_tools():
    """
    Return the list of tools to be used in the chatbot
    """
    api_key = get_tavily_api_key()
    if api_key:
        os.environ["TAVILY_API_KEY"] = api_key
    tools = [TavilySearchResults(max_results=2)]
    return tools

def create_tool_node(tools):
    """
    creates and returns a tool node for the graph
    """
    return ToolNode(tools=tools)