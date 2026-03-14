import streamlit as st
from src.langgraphagentic.ui.streamlite.uiconfigfile import Config


class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
    
    def load_streamlit_ui(self):
        """
        Load and configure the Streamlit UI
        Returns the user input from the chat
        """
        # Page configuration
        st.set_page_config(
            page_title=self.config.get_page_title(),
            page_icon="📊",
            layout="wide"
        )
        
        # Title
        st.title(f"📊 {self.config.get_page_title()}")
        
        # Initialize session state
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        if "thread_id" not in st.session_state:
            st.session_state.thread_id = "streamlit-thread"
        
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Get user input
        user_input = st.chat_input("Ask about stocks or financial news...")
        
        return user_input
