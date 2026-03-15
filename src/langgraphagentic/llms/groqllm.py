import os
import streamlit as st
from langchain_groq import ChatGroq

class GroqLLM:
    def __init__(self, user_controls_input):
        self.user_controls_input = user_controls_input or {}

    def get_llm_model(self):
        try:
            groq_api_key = (
                self.user_controls_input.get("GROQ_API_KEY")
                or (st.secrets.get("GROQ_API_KEY") if hasattr(st, "secrets") else None)
                or os.getenv("GROQ_API_KEY")
                or "your_groq_api_key_here"
            )
            selected_groq_model = (
                self.user_controls_input.get("selected_groq_model")
                or "llama-3.3-70b-versatile"
            )

            if not groq_api_key:
                st.error("Please Enter the Groq API KEY")
                raise ValueError("Groq API key not provided.")

            llm = ChatGroq(api_key=groq_api_key, model=selected_groq_model)
            return llm

        except Exception as e:
            raise ValueError(f"Error occurred with exception: {e}")