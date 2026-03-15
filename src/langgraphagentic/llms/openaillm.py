import os
import streamlit as st
from langchain_openai import ChatOpenAI

class OpenAILLM:
    def __init__(self, user_controls_input):
        self.user_controls_input = user_controls_input or {}

    def get_llm_model(self):
        try:
            openai_api_key = (
                self.user_controls_input.get("OPENAI_API_KEY")
                or (st.secrets.get("OPENAI_API_KEY") if hasattr(st, "secrets") else None)
                or os.getenv("OPENAI_API_KEY")
                or "your_openai_api_key_here"
            )
            selected_openai_model = (
                self.user_controls_input.get("selected_groq_model")
                or "llama-3.3-70b-versatile"
            )

            if not openai_api_key:
                st.error("Please Enter the OpenAI API KEY")
                raise ValueError("OpenAI API key not provided.")

            llm = ChatOpenAI(api_key=openai_api_key, model=selected_openai_model)
            return llm

        except Exception as e:
            raise ValueError(f"Error occurred with exception: {e}")