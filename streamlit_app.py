import streamlit as st
import os
from datetime import datetime
import sys
import json

# Add backend directory to path
sys.path.append('./backend')

# Page configuration
st.set_page_config(
    page_title="Personal Finance Chatbot",
    page_icon="💰",
    layout="wide"
)

def main():
    st.title("💰 Personal Finance Chatbot")
    st.markdown("Welcome to your personal finance assistant!")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Accept user input
    if prompt := st.chat_input("Ask me about your finances..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response (placeholder for now)
        with st.chat_message("assistant"):
            response = f"I understand you asked: '{prompt}'. I'm your personal finance assistant and I'm here to help!"
            st.markdown(response)
            
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
