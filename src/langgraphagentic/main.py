import streamlit as st
from langchain_core.messages import HumanMessage
from src.langgraphagentic.graph.graph_builder import chatbot
from src.langgraphagentic.ui.streamlite.loadui import LoadStreamlitUI
from dotenv import load_dotenv

load_dotenv()

ui = LoadStreamlitUI()
user_input = ui.load_streamlit_ui()

# Process user input
if user_input:
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = chatbot.invoke(
                {"messages": [HumanMessage(content=user_input)]},
                config={"configurable": {"thread_id": st.session_state.thread_id}},
            )
            response = result["messages"][-1].content
            st.markdown(response)
    
    # Add assistant response to session state
    st.session_state.messages.append({"role": "assistant", "content": response})
    
   
