#!/usr/bin/env python3
"""
Flask API Server for Personal Finance Chatbot Frontend
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys
from datetime import datetime

# Add backend directory to path
sys.path.append('./backend')

try:
    from backend.openai_api import OpenAIHandler
    from backend.google_nlu_api import GoogleNLUHandler
    from backend.utils import FinanceUtils
    BACKEND_AVAILABLE = True
except ImportError as e:
    print(f"Backend modules not available: {e}")
    BACKEND_AVAILABLE = False

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Initialize handlers if available
if BACKEND_AVAILABLE:
    openai_handler = OpenAIHandler()
    google_handler = GoogleNLUHandler()
    finance_utils = FinanceUtils()
else:
    openai_handler = None
    google_handler = None
    finance_utils = None

@app.route('/')
def index():
    """Serve the frontend"""
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files from frontend directory"""
    return send_from_directory('frontend', filename)

@app.route('/health', methods=['GET'])
def health_check():
    """Check API and service status"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'openai_status': bool(openai_handler and openai_handler.api_key),
        'google_status': bool(google_handler and google_handler.client),
        'backend_available': BACKEND_AVAILABLE
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Initialize response
        response = {
            'text': '',
            'metadata': {
                'amounts': [],
                'sentiment': 'neutral',
                'timestamp': datetime.now().isoformat()
            }
        }
        
        # Extract amounts if utils available
        if finance_utils:
            amounts = finance_utils.extract_amounts(message)
            response['metadata']['amounts'] = amounts
        
        # Analyze sentiment if Google NLU available
        if google_handler and google_handler.client:
            try:
                sentiment_result = google_handler.analyze_sentiment(message)
                if 'sentiment' in sentiment_result:
                    response['metadata']['sentiment'] = sentiment_result['sentiment']
            except Exception as e:
                print(f"Sentiment analysis error: {e}")
        
        # Generate response using OpenAI if available
        if openai_handler and openai_handler.api_key:
            try:
                ai_response = openai_handler.get_financial_advice(message)
                response['text'] = ai_response
                
                # Add amount highlights if found
                if response['metadata']['amounts']:
                    amounts_str = ", ".join([finance_utils.format_currency(amt) 
                                           for amt in response['metadata']['amounts']])
                    response['text'] += f"\\n\\n💰 I noticed these amounts in your question: {amounts_str}"
                
            except Exception as e:
                print(f"OpenAI API error: {e}")
                response['text'] = generate_fallback_response(message)
        else:
            # Use fallback response
            response['text'] = generate_fallback_response(message)
        
        return jsonify(response)
        
    except Exception as e:
        print(f"Chat error: {e}")
        return jsonify({
            'text': "I apologize, but I'm having trouble processing your request right now. Please try again later.",
            'metadata': {
                'amounts': [],
                'sentiment': 'neutral',
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            }
        }), 500

def generate_fallback_response(message):
    """Generate fallback response when APIs are not available"""
    message_lower = message.lower()
    
    # Financial keywords and responses
    responses = {
        'investment': "Great question about investing! Here are some key principles: 1) Start early to benefit from compound interest, 2) Diversify your portfolio across different asset classes, 3) Consider low-cost index funds for beginners, 4) Only invest money you won't need for at least 5 years. Would you like specific advice based on your risk tolerance?",
        
        'budget': "Creating a budget is essential for financial health! Try the 50/30/20 rule: 50% for needs (rent, utilities, groceries), 30% for wants (entertainment, dining out), and 20% for savings and debt repayment. Track your expenses for a month to see where your money goes, then adjust accordingly.",
        
        'loan': "For loan calculations, the key factors are: principal amount, interest rate, and loan term. For example, a $10,000 loan at 5% annual interest for 5 years would have monthly payments of approximately $188.71. Would you like me to help calculate payments for a specific loan scenario?",
        
        'save': "Smart saving strategies include: 1) Pay yourself first - save before spending, 2) Automate transfers to savings, 3) Build an emergency fund of 3-6 months expenses, 4) Take advantage of high-yield savings accounts, 5) Consider cutting unnecessary subscriptions and expenses.",
        
        'debt': "For debt management: 1) List all debts with balances and interest rates, 2) Consider the debt snowball (pay minimums, extra to smallest) or avalanche method (extra to highest interest), 3) Avoid taking on new debt, 4) Consider debt consolidation if it lowers your interest rate.",
        
        'retirement': "Retirement planning tips: 1) Start as early as possible, 2) Contribute enough to get your employer's 401(k) match, 3) Consider both traditional and Roth IRA options, 4) Aim to save 10-15% of your income, 5) Review and adjust your plan annually."
    }
    
    # Check for keywords and return appropriate response
    for keyword, response in responses.items():
        if keyword in message_lower:
            return response
    
    # Default response
    return f"I understand you're asking about: '{message}'. While I'd love to provide personalized financial advice, I recommend consulting with a qualified financial advisor for your specific situation. However, I can help with general questions about budgeting, saving, investing basics, and financial calculations. What specific area would you like to explore?"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print(f"🚀 Starting Personal Finance Chatbot API Server")
    print(f"📱 Frontend available at: http://localhost:{port}")
    print(f"🔧 Backend available: {BACKEND_AVAILABLE}")
    
    if BACKEND_AVAILABLE:
        print(f"🤖 OpenAI API: {'✅ Connected' if (openai_handler and openai_handler.api_key) else '❌ Not configured'}")
        print(f"🧠 Google NLU: {'✅ Connected' if (google_handler and google_handler.client) else '❌ Not configured'}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
