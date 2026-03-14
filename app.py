import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables FIRST
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)

# Page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="Financial Research Assistant",
    page_icon="📊",
    layout="centered"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Main container */
    .main-header {
        text-align: center;
        padding: 2rem 0;
    }
    
    /* Welcome title */
    .welcome-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    /* Subtitle */
    .welcome-subtitle {
        font-size: 1.1rem;
        color: #6b7280;
        margin-bottom: 2rem;
    }
    
    /* Quick action buttons container */
    .quick-actions {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        justify-content: center;
        margin: 1.5rem 0;
    }
    
    /* Style for stButton */
    div.stButton > button {
        border-radius: 20px;
        padding: 0.5rem 1rem;
        font-size: 0.9rem;
        border: 1px solid #e5e7eb;
        background-color: #f9fafb;
        transition: all 0.2s;
    }
    
    div.stButton > button:hover {
        background-color: #f3f4f6;
        border-color: #667eea;
        color: #667eea;
    }
    
    /* Chat messages styling */
    .stChatMessage {
        padding: 1rem;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Import after dotenv is loaded
from langchain_core.messages import HumanMessage
from src.langgraphagentic.graph.graph_builder import chatbot

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = "streamlit-thread"

# Function to handle button clicks
def handle_quick_action(query):
    st.session_state.quick_query = query

# Welcome screen (show only when no messages)
if len(st.session_state.messages) == 0:
    st.markdown("""
    <div class="main-header">
        <div class="welcome-title">Welcome to Financial Research Assistant</div>
        <div class="welcome-subtitle">Ask any question about stock prices, earnings dates, company info, or financial news.</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick action buttons
    st.markdown("#### 💡 Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🍎 Apple stock news", use_container_width=True):
            handle_quick_action("What's the latest news about Apple stock?")
        if st.button("📈 NVIDIA AI updates", use_container_width=True):
            handle_quick_action("Tell me about NVIDIA AI updates and stock performance")
    
    with col2:
        if st.button("📦 Amazon earnings", use_container_width=True):
            handle_quick_action("When is Amazon's next earnings date?")
        if st.button("💻 Intel restructuring", use_container_width=True):
            handle_quick_action("What's happening with Intel restructuring?")
    
    with col3:
        if st.button("🤖 Microsoft AI", use_container_width=True):
            handle_quick_action("Latest Microsoft AI news and stock price")
        if st.button("🎬 Netflix growth", use_container_width=True):
            handle_quick_action("How is Netflix stock performing?")
    
    st.markdown("---")

else:
    # Show title when in chat mode
    st.markdown("### 📊 Financial Research Assistant")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle quick action query
if "quick_query" in st.session_state and st.session_state.quick_query:
    prompt = st.session_state.quick_query
    st.session_state.quick_query = None  # Clear it
    
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("🔍 Researching..."):
            result = chatbot.invoke(
                {"messages": [HumanMessage(content=prompt)]},
                config={"configurable": {"thread_id": st.session_state.thread_id}},
            )
            response = result["messages"][-1].content
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

# Chat input
if prompt := st.chat_input("Ask about stocks, earnings, or financial news..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("🔍 Researching..."):
            result = chatbot.invoke(
                {"messages": [HumanMessage(content=prompt)]},
                config={"configurable": {"thread_id": st.session_state.thread_id}},
            )
            response = result["messages"][-1].content
            st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar with info
with st.sidebar:
    st.markdown("### 📊 About")
    st.markdown("""
    **Financial Research Assistant** helps you:
    - 📈 Get real-time stock prices
    - 📅 Find earnings dates
    - 🏢 Research company info
    - 📰 Search financial news
    """)
    
    st.markdown("---")
    st.markdown("### 🔧 Powered by")
    st.markdown("""
    - OpenAI GPT-4o-mini
    - Alpha Vantage API
    - Tavily Search
    - LangGraph
    """)
    
    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()