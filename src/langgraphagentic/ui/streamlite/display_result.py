import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage


class DisplayResultStreamlit:
    def __init__(self, graph, user_message):
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self):
        """
        Display chatbot results with tool call visibility
        """
        # Invoke the graph
        result = self.graph.invoke(
            {"messages": [HumanMessage(content=self.user_message)]},
            config={"configurable": {"thread_id": st.session_state.thread_id}},
        )
        
        # Display messages
        for message in result['messages']:
            if isinstance(message, HumanMessage):
                with st.chat_message("user"):
                    st.write(message.content)
                    
            elif isinstance(message, ToolMessage):
                with st.expander("🔧 Tool Call Details", expanded=False):
                    st.json(message.content if isinstance(message.content, dict) else {"result": message.content})
                    
            elif isinstance(message, AIMessage) and message.content:
                with st.chat_message("assistant"):
                    st.write(message.content)
        
        # Return the last AI response
        return result['messages'][-1].content
