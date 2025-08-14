"""
Personal Finance Chatbot - Modern Tkinter GUI Frontend
A professional desktop application with modern UI design
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import queue
import datetime
import sys
import os

# Add backend to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

try:
    from main import PersonalFinanceChatbot
    from utils import extract_amounts, format_currency
    BACKEND_AVAILABLE = True
except ImportError:
    BACKEND_AVAILABLE = False
    print("Backend modules not available, running in demo mode")


class ModernChatGUI:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_styles()
        self.create_widgets()
        self.setup_layout()
        
        # Initialize chatbot
        if BACKEND_AVAILABLE:
            self.chatbot = PersonalFinanceChatbot()
            self.check_api_status()
        else:
            self.chatbot = None
            
        # Threading for async operations
        self.response_queue = queue.Queue()
        self.root.after(100, self.check_response_queue)
        
    def setup_window(self):
        """Configure main window properties"""
        self.root.title("💰 Personal Finance Chatbot")
        self.root.geometry("900x700")
        self.root.minsize(600, 500)
        
        # Center window on screen
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Configure window icon and colors
        self.root.configure(bg='#f0f2f5')
        
    def setup_styles(self):
        """Configure modern ttk styles"""
        style = ttk.Style()
        
        # Configure modern button style
        style.configure(
            'Modern.TButton',
            background='#0084ff',
            foreground='white',
            borderwidth=0,
            focuscolor='none',
            font=('Helvetica', 10, 'bold')
        )
        style.map('Modern.TButton',
                 background=[('active', '#0066cc'),
                           ('pressed', '#004499')])
        
        # Configure entry style
        style.configure(
            'Modern.TEntry',
            fieldbackground='white',
            borderwidth=1,
            insertcolor='#0084ff'
        )
        
    def create_widgets(self):
        """Create all GUI widgets"""
        # Header frame
        self.header_frame = tk.Frame(self.root, bg='#0084ff', height=60)
        self.header_frame.pack_propagate(False)
        
        # Title label
        self.title_label = tk.Label(
            self.header_frame,
            text="💰 Personal Finance Assistant",
            font=('Helvetica', 16, 'bold'),
            bg='#0084ff',
            fg='white'
        )
        
        # Status frame in header
        self.status_frame = tk.Frame(self.header_frame, bg='#0084ff')
        self.api_status_label = tk.Label(
            self.status_frame,
            text="🔄 Checking APIs...",
            font=('Helvetica', 9),
            bg='#0084ff',
            fg='white'
        )
        
        # Main content frame
        self.main_frame = tk.Frame(self.root, bg='#f0f2f5')
        
        # Chat display area
        self.chat_frame = tk.Frame(self.main_frame, bg='white', relief='solid', bd=1)
        
        self.chat_display = scrolledtext.ScrolledText(
            self.chat_frame,
            wrap=tk.WORD,
            font=('Helvetica', 11),
            bg='white',
            fg='#333333',
            selectbackground='#e3f2fd',
            relief='flat',
            padx=15,
            pady=10
        )
        
        # Input frame
        self.input_frame = tk.Frame(self.main_frame, bg='#f0f2f5')
        
        # Message entry
        self.message_var = tk.StringVar()
        self.message_entry = ttk.Entry(
            self.input_frame,
            textvariable=self.message_var,
            font=('Helvetica', 11),
            style='Modern.TEntry'
        )
        
        # Send button
        self.send_button = ttk.Button(
            self.input_frame,
            text="Send",
            command=self.send_message,
            style='Modern.TButton'
        )
        
        # Quick action buttons frame
        self.actions_frame = tk.Frame(self.main_frame, bg='#f0f2f5')
        
        self.quick_buttons = []
        quick_actions = [
            "💰 Help me create a budget",
            "📊 Investment advice for beginners",
            "💳 Should I pay off debt first?",
            "🏠 Saving for a house down payment"
        ]
        
        for i, action in enumerate(quick_actions):
            btn = tk.Button(
                self.actions_frame,
                text=action,
                command=lambda a=action: self.quick_action(a),
                bg='#e8f4fd',
                fg='#0084ff',
                border=0,
                font=('Helvetica', 9),
                cursor='hand2',
                activebackground='#d0e9ff',
                relief='flat',
                pady=8
            )
            self.quick_buttons.append(btn)
            
        # Bind enter key to send message
        self.root.bind('<Return>', lambda e: self.send_message())
        
    def setup_layout(self):
        """Arrange widgets using grid layout"""
        # Header
        self.header_frame.pack(fill='x')
        self.title_label.pack(side='left', padx=20, pady=15)
        self.status_frame.pack(side='right', padx=20, pady=15)
        self.api_status_label.pack()
        
        # Main content
        self.main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Chat area
        self.chat_frame.pack(fill='both', expand=True, pady=(0, 10))
        self.chat_display.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Quick actions
        self.actions_frame.pack(fill='x', pady=(0, 10))
        for i, btn in enumerate(self.quick_buttons):
            btn.pack(side='left', fill='x', expand=True, padx=2)
            
        # Input area
        self.input_frame.pack(fill='x')
        self.message_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        self.send_button.pack(side='right')
        
        # Initial welcome message
        self.add_message("Assistant", 
                        "Hello! 👋 I'm your Personal Finance Assistant. "
                        "I can help you with budgeting, investing, debt management, and more!\n\n"
                        "You can type a question or use the quick action buttons below.",
                        "#f0f8ff")
        
    def check_api_status(self):
        """Check and display API connection status"""
        def check_apis():
            status_parts = []
            
            # Check OpenAI API
            if hasattr(self.chatbot, 'openai_client') and self.chatbot.openai_client:
                status_parts.append("🟢 OpenAI")
            else:
                status_parts.append("🔴 OpenAI")
                
            # Check Google NLU
            if hasattr(self.chatbot, 'nlu_client') and self.chatbot.nlu_client:
                status_parts.append("🟢 Google NLU")
            else:
                status_parts.append("🔴 Google NLU")
                
            status_text = " | ".join(status_parts)
            self.response_queue.put(('status', status_text))
            
        if self.chatbot:
            thread = threading.Thread(target=check_apis, daemon=True)
            thread.start()
        else:
            self.api_status_label.config(text="🔴 Demo Mode")
            
    def add_message(self, sender, message, bg_color="#ffffff"):
        """Add a message to the chat display with styling"""
        timestamp = datetime.datetime.now().strftime("%H:%M")
        
        # Configure text tags for styling
        self.chat_display.tag_configure("sender", font=('Helvetica', 10, 'bold'))
        self.chat_display.tag_configure("timestamp", font=('Helvetica', 8), foreground='#888888')
        self.chat_display.tag_configure("message", font=('Helvetica', 11))
        self.chat_display.tag_configure("amount", foreground='#00a651', font=('Helvetica', 11, 'bold'))
        
        # Insert message
        self.chat_display.insert('end', f"{sender}", "sender")
        self.chat_display.insert('end', f" • {timestamp}\n", "timestamp")
        
        # Highlight financial amounts in the message
        if BACKEND_AVAILABLE:
            amounts = extract_amounts(message)
            if amounts:
                words = message.split()
                for word in words:
                    if any(str(amount) in word.replace(',', '').replace('$', '') for amount in amounts):
                        self.chat_display.insert('end', f"{word} ", "amount")
                    else:
                        self.chat_display.insert('end', f"{word} ", "message")
            else:
                self.chat_display.insert('end', message, "message")
        else:
            self.chat_display.insert('end', message, "message")
            
        self.chat_display.insert('end', "\n\n")
        self.chat_display.see('end')
        
    def quick_action(self, action):
        """Handle quick action button clicks"""
        # Remove emoji and send as message
        clean_action = action.split(' ', 1)[1] if ' ' in action else action
        self.message_var.set(clean_action)
        self.send_message()
        
    def send_message(self):
        """Send message and get response"""
        user_message = self.message_var.get().strip()
        if not user_message:
            return
            
        # Display user message
        self.add_message("You", user_message, "#e3f2fd")
        self.message_var.set("")
        
        # Show typing indicator
        self.add_message("Assistant", "Typing...", "#f0f8ff")
        
        # Get response in background thread
        def get_response():
            try:
                if self.chatbot and BACKEND_AVAILABLE:
                    response = self.chatbot.get_response(user_message)
                else:
                    # Demo response
                    response = self.get_demo_response(user_message)
                    
                self.response_queue.put(('response', response))
            except Exception as e:
                self.response_queue.put(('error', str(e)))
                
        thread = threading.Thread(target=get_response, daemon=True)
        thread.start()
        
    def get_demo_response(self, message):
        """Generate demo responses when backend isn't available"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['budget', 'budgeting']):
            return ("Creating a budget is essential for financial health! Here's a simple approach:\n\n"
                   "1. Track your income and expenses for a month\n"
                   "2. Use the 50/30/20 rule: 50% needs, 30% wants, 20% savings\n"
                   "3. Start with essential categories: housing, food, transportation\n"
                   "4. Set realistic savings goals\n\n"
                   "Would you like help with any specific budgeting category?")
                   
        elif any(word in message_lower for word in ['invest', 'investment']):
            return ("Great question about investing! For beginners, consider:\n\n"
                   "1. Start with an emergency fund (3-6 months expenses)\n"
                   "2. Consider low-cost index funds or ETFs\n"
                   "3. Take advantage of employer 401(k) matching\n"
                   "4. Diversify your portfolio\n"
                   "5. Think long-term and don't panic during market dips\n\n"
                   "Remember: invest only what you can afford to lose!")
                   
        elif any(word in message_lower for word in ['debt', 'loan']):
            return ("Managing debt effectively is crucial! Here's my advice:\n\n"
                   "1. List all debts with balances and interest rates\n"
                   "2. Pay minimums on all debts\n"
                   "3. Use debt avalanche (highest interest first) or snowball (smallest balance first)\n"
                   "4. Consider debt consolidation if it lowers rates\n"
                   "5. Avoid taking on new debt while paying off existing debt\n\n"
                   "Would you like help prioritizing your specific debts?")
                   
        else:
            return ("Thanks for your question! I can help with:\n\n"
                   "💰 Budgeting and expense tracking\n"
                   "📈 Investment strategies and portfolio advice\n"
                   "💳 Debt management and payoff strategies\n"
                   "🏠 Saving for major purchases\n"
                   "📊 Financial planning and goal setting\n\n"
                   "What specific financial topic would you like to explore?")
                   
    def check_response_queue(self):
        """Check for responses from background threads"""
        try:
            while True:
                response_type, data = self.response_queue.get_nowait()
                
                if response_type == 'response':
                    # Remove typing indicator
                    self.chat_display.delete('end-3l', 'end-1l')
                    # Add actual response
                    self.add_message("Assistant", data, "#f0f8ff")
                    
                elif response_type == 'error':
                    self.chat_display.delete('end-3l', 'end-1l')
                    self.add_message("Assistant", 
                                   f"Sorry, I encountered an error: {data}\n"
                                   "Please try again or check your API configuration.",
                                   "#ffe6e6")
                                   
                elif response_type == 'status':
                    self.api_status_label.config(text=data)
                    
        except queue.Empty:
            pass
            
        # Schedule next check
        self.root.after(100, self.check_response_queue)


def main():
    """Main application entry point"""
    root = tk.Tk()
    app = ModernChatGUI(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
        root.quit()


if __name__ == "__main__":
    main()
