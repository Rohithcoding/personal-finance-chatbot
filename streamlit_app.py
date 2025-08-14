import streamlit as st
import os
from datetime import datetime
import sys
import json

# Add backend directory to path
sys.path.append('./backend')

try:
    from backend.openai_api import OpenAIHandler
    from backend.google_nlu_api import GoogleNLUHandler
    from backend.utils import FinanceUtils
except ImportError as e:
    st.error(f"Error importing backend modules: {e}")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Personal Finance Chatbot",
    page_icon="💰",
    layout="wide"
)

# Initialize handlers
@st.cache_resource
def initialize_handlers():
    return {
        'openai': OpenAIHandler(),
        'google_nlu': GoogleNLUHandler(),
        'utils': FinanceUtils()
    }

def main():
    st.title("💰 Personal Finance Chatbot")
    st.markdown("Welcome to your personal finance assistant!")
    
    # Initialize handlers
    handlers = initialize_handlers()
    
    # Sidebar with app info
    with st.sidebar:
        st.header("About")
        st.markdown("""
        This chatbot can help you with:
        - Financial advice and planning
        - Investment guidance
        - Loan calculations
        - Budgeting tips
        - Expense analysis
        """)
        
        # Check API status
        st.header("API Status")
        openai_status = "✅ Connected" if handlers['openai'].api_key else "❌ Not configured"
        google_status = "✅ Connected" if handlers['google_nlu'].client else "❌ Not configured"
        
        st.write(f"OpenAI: {openai_status}")
        st.write(f"Google NLU: {google_status}")
    
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
        
        # Generate response using OpenAI
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Analyze sentiment
                sentiment_result = handlers['google_nlu'].analyze_sentiment(prompt)
                
                # Generate response using OpenAI
                if handlers['openai'].api_key:
                    response = handlers['openai'].get_financial_advice(prompt)
                else:
                    response = "I'd love to help with your financial question, but the OpenAI API is not configured. Please check your environment variables."
                
                # Extract any financial amounts for analysis
                amounts = handlers['utils'].extract_amounts(prompt)
                if amounts:
                    amounts_str = ", ".join([handlers['utils'].format_currency(amt) for amt in amounts])
                    response += f"\n\n💰 I noticed these amounts in your question: {amounts_str}"
                
                # Add sentiment info if available
                if sentiment_result and 'sentiment' in sentiment_result:
                    sentiment_emoji = {"positive": "😊", "negative": "😔", "neutral": "😐"}.get(sentiment_result['sentiment'], "")
                    response += f"\n\n{sentiment_emoji} Sentiment: {sentiment_result['sentiment'].title()}"
            
            st.markdown(response)
            
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
