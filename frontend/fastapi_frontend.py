"""
Personal Finance Chatbot - FastAPI Python Web Frontend
Modern web interface built entirely in Python using FastAPI and Jinja2 templates
"""

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import sys
import os
from typing import List, Dict
import datetime
import json

# Add backend to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

try:
    from main import PersonalFinanceChatbot
    from utils import extract_amounts, format_currency
    BACKEND_AVAILABLE = True
except ImportError:
    BACKEND_AVAILABLE = False
    print("Backend modules not available, running in demo mode")

# Initialize FastAPI app
app = FastAPI(title="Personal Finance Chatbot", description="AI-powered financial assistant")

# Create templates directory if it doesn't exist
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
os.makedirs(templates_dir, exist_ok=True)

templates = Jinja2Templates(directory=templates_dir)

# Initialize chatbot
if BACKEND_AVAILABLE:
    chatbot = PersonalFinanceChatbot()
else:
    chatbot = None

# In-memory conversation storage (use database in production)
conversations: Dict[str, List[Dict]] = {}


class ChatMessage:
    def __init__(self, sender: str, message: str, timestamp: str = None):
        self.sender = sender
        self.message = message
        self.timestamp = timestamp or datetime.datetime.now().strftime("%H:%M:%S")
        
    def to_dict(self):
        return {
            "sender": self.sender,
            "message": self.message,
            "timestamp": self.timestamp
        }


def get_demo_response(message: str) -> str:
    """Generate demo responses when backend isn't available"""
    message_lower = message.lower()
    
    if any(word in message_lower for word in ['budget', 'budgeting']):
        return ("Creating a budget is essential for financial health! Here's a simple approach:\n\n"
               "• Track your income and expenses for a month\n"
               "• Use the 50/30/20 rule: 50% needs, 30% wants, 20% savings\n"
               "• Start with essential categories: housing, food, transportation\n"
               "• Set realistic savings goals\n\n"
               "Would you like help with any specific budgeting category?")
               
    elif any(word in message_lower for word in ['invest', 'investment']):
        return ("Great question about investing! For beginners, consider:\n\n"
               "• Start with an emergency fund (3-6 months expenses)\n"
               "• Consider low-cost index funds or ETFs\n"
               "• Take advantage of employer 401(k) matching\n"
               "• Diversify your portfolio\n"
               "• Think long-term and don't panic during market dips\n\n"
               "Remember: invest only what you can afford to lose!")
               
    elif any(word in message_lower for word in ['debt', 'loan']):
        return ("Managing debt effectively is crucial! Here's my advice:\n\n"
               "• List all debts with balances and interest rates\n"
               "• Pay minimums on all debts\n"
               "• Use debt avalanche (highest interest first) or snowball (smallest balance first)\n"
               "• Consider debt consolidation if it lowers rates\n"
               "• Avoid taking on new debt while paying off existing debt\n\n"
               "Would you like help prioritizing your specific debts?")
               
    elif any(word in message_lower for word in ['save', 'saving']):
        return ("Smart saving strategies can accelerate your financial goals:\n\n"
               "• Automate savings - pay yourself first\n"
               "• Use high-yield savings accounts\n"
               "• Set specific, measurable savings goals\n"
               "• Track your progress regularly\n"
               "• Consider the 52-week savings challenge\n\n"
               "What are you saving for? I can help you create a plan!")
               
    else:
        return ("Thanks for your question! I can help with:\n\n"
               "💰 Budgeting and expense tracking\n"
               "📈 Investment strategies and portfolio advice\n"
               "💳 Debt management and payoff strategies\n"
               "🏠 Saving for major purchases\n"
               "📊 Financial planning and goal setting\n\n"
               "What specific financial topic would you like to explore?")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with chat interface"""
    session_id = "default"  # In production, use proper session management
    
    # Initialize conversation if doesn't exist
    if session_id not in conversations:
        conversations[session_id] = []
        # Add welcome message
        welcome_msg = ChatMessage(
            "Assistant", 
            "Hello! 👋 I'm your Personal Finance Assistant. I can help you with budgeting, investing, debt management, and more! What would you like to discuss today?"
        )
        conversations[session_id].append(welcome_msg.to_dict())
    
    return templates.TemplateResponse("chat.html", {
        "request": request,
        "messages": conversations[session_id],
        "backend_available": BACKEND_AVAILABLE
    })


@app.post("/chat")
async def chat(request: Request, message: str = Form(...)):
    """Handle chat messages"""
    session_id = "default"  # In production, use proper session management
    
    if session_id not in conversations:
        conversations[session_id] = []
    
    # Add user message
    user_msg = ChatMessage("You", message)
    conversations[session_id].append(user_msg.to_dict())
    
    # Generate response
    try:
        if chatbot and BACKEND_AVAILABLE:
            response = chatbot.get_response(message)
        else:
            response = get_demo_response(message)
    except Exception as e:
        response = f"Sorry, I encountered an error: {str(e)}\nPlease try again or check your API configuration."
    
    # Add assistant response
    assistant_msg = ChatMessage("Assistant", response)
    conversations[session_id].append(assistant_msg.to_dict())
    
    return RedirectResponse(url="/", status_code=303)


@app.get("/api/status")
async def api_status():
    """Get API status"""
    status = {
        "backend_available": BACKEND_AVAILABLE,
        "openai_available": False,
        "google_nlu_available": False
    }
    
    if chatbot and BACKEND_AVAILABLE:
        try:
            status["openai_available"] = hasattr(chatbot, 'openai_client') and chatbot.openai_client is not None
            status["google_nlu_available"] = hasattr(chatbot, 'nlu_client') and chatbot.nlu_client is not None
        except:
            pass
    
    return status


@app.get("/clear")
async def clear_chat():
    """Clear chat history"""
    session_id = "default"
    if session_id in conversations:
        conversations[session_id] = []
    return RedirectResponse(url="/", status_code=303)


def create_chat_template():
    """Create the HTML template for the chat interface"""
    template_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>💰 Personal Finance Chatbot</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        .header {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 1rem 2rem;
            box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .header h1 {
            color: #333;
            font-size: 1.5rem;
            font-weight: 600;
        }

        .status {
            display: flex;
            gap: 1rem;
            font-size: 0.9rem;
            color: #666;
        }

        .container {
            flex: 1;
            display: flex;
            flex-direction: column;
            max-width: 800px;
            margin: 2rem auto;
            padding: 0 1rem;
            width: 100%;
        }

        .chat-container {
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
            flex: 1;
            display: flex;
            flex-direction: column;
            min-height: 500px;
        }

        .chat-messages {
            flex: 1;
            padding: 2rem;
            overflow-y: auto;
            max-height: 400px;
        }

        .message {
            margin-bottom: 1.5rem;
            animation: fadeIn 0.3s ease-in;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .message-header {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 0.5rem;
        }

        .sender {
            font-weight: 600;
            color: #333;
        }

        .timestamp {
            font-size: 0.8rem;
            color: #888;
        }

        .message-content {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 10px;
            line-height: 1.5;
            white-space: pre-line;
        }

        .message.assistant .message-content {
            background: linear-gradient(135deg, #e3f2fd 0%, #f0f8ff 100%);
            border-left: 4px solid #2196f3;
        }

        .message.user .message-content {
            background: linear-gradient(135deg, #e8f5e8 0%, #f0fff0 100%);
            border-left: 4px solid #4caf50;
        }

        .input-section {
            padding: 1.5rem;
            border-top: 1px solid #eee;
        }

        .quick-actions {
            display: flex;
            gap: 0.5rem;
            margin-bottom: 1rem;
            flex-wrap: wrap;
        }

        .quick-btn {
            background: #e3f2fd;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            color: #1976d2;
            cursor: pointer;
            font-size: 0.9rem;
            transition: all 0.2s ease;
        }

        .quick-btn:hover {
            background: #2196f3;
            color: white;
            transform: translateY(-2px);
        }

        .input-form {
            display: flex;
            gap: 1rem;
        }

        .message-input {
            flex: 1;
            padding: 1rem;
            border: 2px solid #e0e0e0;
            border-radius: 25px;
            font-size: 1rem;
            outline: none;
            transition: border-color 0.2s ease;
        }

        .message-input:focus {
            border-color: #2196f3;
        }

        .send-btn {
            background: linear-gradient(135deg, #2196f3 0%, #21cbf3 100%);
            color: white;
            border: none;
            padding: 1rem 2rem;
            border-radius: 25px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .send-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(33, 150, 243, 0.3);
        }

        .actions {
            display: flex;
            gap: 1rem;
            justify-content: center;
            margin-top: 1rem;
        }

        .action-btn {
            background: rgba(255, 255, 255, 0.9);
            color: #333;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            cursor: pointer;
            text-decoration: none;
            transition: all 0.2s ease;
        }

        .action-btn:hover {
            background: white;
            transform: translateY(-1px);
        }

        @media (max-width: 600px) {
            .container {
                margin: 1rem auto;
                padding: 0 0.5rem;
            }
            
            .input-form {
                flex-direction: column;
            }
            
            .quick-actions {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>💰 Personal Finance Chatbot</h1>
        <div class="status">
            {% if backend_available %}
                <span>🟢 Backend Connected</span>
            {% else %}
                <span>🟡 Demo Mode</span>
            {% endif %}
        </div>
    </div>

    <div class="container">
        <div class="chat-container">
            <div class="chat-messages">
                {% for message in messages %}
                <div class="message {{ message.sender.lower() }}">
                    <div class="message-header">
                        <span class="sender">{{ message.sender }}</span>
                        <span class="timestamp">{{ message.timestamp }}</span>
                    </div>
                    <div class="message-content">{{ message.message }}</div>
                </div>
                {% endfor %}
            </div>

            <div class="input-section">
                <div class="quick-actions">
                    <button class="quick-btn" onclick="sendQuickMessage('Help me create a budget')">💰 Budget Help</button>
                    <button class="quick-btn" onclick="sendQuickMessage('Investment advice for beginners')">📈 Investing</button>
                    <button class="quick-btn" onclick="sendQuickMessage('Should I pay off debt first?')">💳 Debt Strategy</button>
                    <button class="quick-btn" onclick="sendQuickMessage('Saving for a house down payment')">🏠 Save for Home</button>
                </div>

                <form method="post" action="/chat" class="input-form">
                    <input 
                        type="text" 
                        name="message" 
                        class="message-input" 
                        placeholder="Ask me anything about personal finance..."
                        required
                        autofocus
                    >
                    <button type="submit" class="send-btn">Send</button>
                </form>
            </div>
        </div>

        <div class="actions">
            <a href="/clear" class="action-btn">🗑️ Clear Chat</a>
            <a href="/api/status" class="action-btn">📊 API Status</a>
        </div>
    </div>

    <script>
        function sendQuickMessage(message) {
            const input = document.querySelector('.message-input');
            input.value = message;
            document.querySelector('.input-form').submit();
        }

        // Auto-scroll to bottom
        const chatMessages = document.querySelector('.chat-messages');
        chatMessages.scrollTop = chatMessages.scrollHeight;

        // Focus on input
        document.querySelector('.message-input').focus();
    </script>
</body>
</html>'''
    
    template_path = os.path.join(templates_dir, "chat.html")
    with open(template_path, "w", encoding="utf-8") as f:
        f.write(template_content)


def main():
    """Run the FastAPI application"""
    # Create template file
    create_chat_template()
    
    print("🚀 Starting Personal Finance Chatbot - FastAPI Frontend")
    print(f"📁 Templates directory: {templates_dir}")
    print(f"🔧 Backend available: {BACKEND_AVAILABLE}")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        log_level="info"
    )


if __name__ == "__main__":
    main()
