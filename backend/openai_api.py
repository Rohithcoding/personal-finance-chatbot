"""
OpenAI API integration for personal finance chatbot
"""

import os
import openai
from typing import Dict, List

class OpenAIHandler:
    """Handle OpenAI API interactions"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if self.api_key:
            openai.api_key = self.api_key
    
    def generate_response(self, messages: List[Dict[str, str]], model: str = "gpt-3.5-turbo") -> str:
        """Generate response using OpenAI API"""
        try:
            if not self.api_key:
                return "OpenAI API key not configured. Please check your environment variables."
            
            response = openai.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def get_financial_advice(self, query: str) -> str:
        """Get financial advice for a specific query"""
        system_message = {
            "role": "system",
            "content": """You are a helpful personal finance assistant. 
            Provide clear, practical financial advice. Be concise but comprehensive.
            Always remind users to consult with financial professionals for major decisions."""
        }
        
        user_message = {
            "role": "user", 
            "content": query
        }
        
        messages = [system_message, user_message]
        return self.generate_response(messages)
