import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables FIRST
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)

# Page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="AGENTIC: Financial Research Assistant",
    page_icon="📊"
)

st.title("📊 AGENTIC: Financial Research Assistant")

# Import after dotenv is loaded
from langchain_core.messages import HumanMessage
from src.langgraphagentic.graph.graph_builder import chatbot

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = "streamlit-thread"

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about stocks or financial news..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = chatbot.invoke(
                {"messages": [HumanMessage(content=prompt)]},
                config={"configurable": {"thread_id": st.session_state.thread_id}},
            )
            response = result["messages"][-1].content
            st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})