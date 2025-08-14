"""
Personal Finance Chatbot - Kivy Mobile-Style Frontend
Modern mobile-like interface using Kivy for cross-platform deployment
"""

try:
    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.scrollview import ScrollView
    from kivy.uix.label import Label
    from kivy.uix.textinput import TextInput
    from kivy.uix.button import Button
    from kivy.uix.gridlayout import GridLayout
    from kivy.uix.screenmanager import ScreenManager, Screen
    from kivy.clock import Clock
    from kivy.metrics import dp
    from kivy.graphics import Color, RoundedRectangle
    from kivy.core.window import Window
    KIVY_AVAILABLE = True
except ImportError:
    KIVY_AVAILABLE = False
    print("Kivy not installed. Install with: pip install kivy")

import sys
import os
import threading
import datetime

# Add backend to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

try:
    from main import PersonalFinanceChatbot
    from utils import extract_amounts, format_currency
    BACKEND_AVAILABLE = True
except ImportError:
    BACKEND_AVAILABLE = False
    print("Backend modules not available, running in demo mode")


class MessageBubble(BoxLayout):
    """Custom widget for chat message bubbles"""
    
    def __init__(self, sender, message, timestamp=None, **kwargs):
        super().__init__(orientation='vertical', size_hint_y=None, **kwargs)
        self.spacing = dp(5)
        self.padding = [dp(10), dp(5)]
        
        # Set height based on content
        self.bind(minimum_height=self.setter('height'))
        
        # Header with sender and timestamp
        header = BoxLayout(size_hint_y=None, height=dp(20))
        sender_label = Label(
            text=sender,
            font_size=dp(12),
            bold=True,
            size_hint_y=None,
            height=dp(20),
            text_size=(None, None),
            halign='left'
        )
        
        if not timestamp:
            timestamp = datetime.datetime.now().strftime("%H:%M")
        
        time_label = Label(
            text=timestamp,
            font_size=dp(10),
            color=(0.7, 0.7, 0.7, 1),
            size_hint_y=None,
            height=dp(20),
            text_size=(None, None),
            halign='right'
        )
        
        header.add_widget(sender_label)
        header.add_widget(time_label)
        self.add_widget(header)
        
        # Message content
        message_label = Label(
            text=message,
            font_size=dp(14),
            text_size=(Window.width - dp(40), None),
            halign='left',
            valign='top',
            size_hint_y=None
        )
        message_label.bind(texture_size=message_label.setter('size'))
        
        # Style based on sender
        with message_label.canvas.before:
            if sender == "You":
                Color(0.85, 0.95, 0.85, 1)  # Light green for user
            else:
                Color(0.9, 0.95, 1, 1)  # Light blue for assistant
            
            self.rect = RoundedRectangle(
                pos=message_label.pos,
                size=message_label.size,
                radius=[dp(10)]
            )
            
        message_label.bind(pos=self.update_rect, size=self.update_rect)
        self.add_widget(message_label)
        
    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class ChatScreen(Screen):
    """Main chat interface screen"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.chatbot = None
        if BACKEND_AVAILABLE:
            try:
                self.chatbot = PersonalFinanceChatbot()
            except Exception as e:
                print(f"Failed to initialize chatbot: {e}")
        
        self.setup_ui()
        self.add_welcome_message()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main layout
        main_layout = BoxLayout(orientation='vertical', spacing=dp(5))
        
        # Header
        header = BoxLayout(
            size_hint_y=None,
            height=dp(60),
            spacing=dp(10),
            padding=[dp(10), dp(5)]
        )
        
        # Title
        title_label = Label(
            text='💰 Personal Finance Assistant',
            font_size=dp(18),
            bold=True,
            size_hint_x=0.8
        )
        
        # Status indicator
        status_text = "🟢 Ready" if BACKEND_AVAILABLE else "🟡 Demo Mode"
        self.status_label = Label(
            text=status_text,
            font_size=dp(12),
            size_hint_x=0.2
        )
        
        header.add_widget(title_label)
        header.add_widget(self.status_label)
        main_layout.add_widget(header)
        
        # Chat messages area
        self.scroll = ScrollView()
        self.chat_layout = GridLayout(cols=1, size_hint_y=None, spacing=dp(5))
        self.chat_layout.bind(minimum_height=self.chat_layout.setter('height'))
        
        self.scroll.add_widget(self.chat_layout)
        main_layout.add_widget(self.scroll)
        
        # Quick action buttons
        quick_layout = GridLayout(
            cols=2,
            size_hint_y=None,
            height=dp(80),
            spacing=dp(5),
            padding=[dp(10), dp(5)]
        )
        
        quick_actions = [
            "💰 Budget Help",
            "📈 Investment Tips",
            "💳 Debt Strategy", 
            "🏠 Saving Goals"
        ]
        
        for action in quick_actions:
            btn = Button(
                text=action,
                font_size=dp(12),
                background_color=(0.2, 0.6, 1, 1),
                size_hint_y=None,
                height=dp(35)
            )
            btn.bind(on_press=lambda x, text=action: self.quick_action(text))
            quick_layout.add_widget(btn)
            
        main_layout.add_widget(quick_layout)
        
        # Input area
        input_layout = BoxLayout(
            size_hint_y=None,
            height=dp(50),
            spacing=dp(5),
            padding=[dp(10), dp(5)]
        )
        
        self.text_input = TextInput(
            hint_text='Ask me anything about personal finance...',
            multiline=False,
            font_size=dp(14),
            size_hint_x=0.8
        )
        self.text_input.bind(on_text_validate=self.send_message)
        
        send_btn = Button(
            text='Send',
            font_size=dp(14),
            background_color=(0.2, 0.8, 0.2, 1),
            size_hint_x=0.2
        )
        send_btn.bind(on_press=self.send_message)
        
        input_layout.add_widget(self.text_input)
        input_layout.add_widget(send_btn)
        main_layout.add_widget(input_layout)
        
        self.add_widget(main_layout)
        
    def add_welcome_message(self):
        """Add welcome message to chat"""
        welcome_text = (
            "Hello! 👋 I'm your Personal Finance Assistant.\n\n"
            "I can help you with:\n"
            "• Budgeting and expense tracking\n"
            "• Investment strategies\n" 
            "• Debt management\n"
            "• Saving for goals\n\n"
            "What would you like to discuss today?"
        )
        self.add_message("Assistant", welcome_text)
        
    def add_message(self, sender, message):
        """Add a message to the chat"""
        bubble = MessageBubble(sender, message)
        self.chat_layout.add_widget(bubble)
        
        # Scroll to bottom
        Clock.schedule_once(self.scroll_to_bottom, 0.1)
        
    def scroll_to_bottom(self, dt):
        """Scroll chat to bottom"""
        self.scroll.scroll_y = 0
        
    def quick_action(self, action_text):
        """Handle quick action button press"""
        # Remove emoji and send as message
        clean_text = action_text.split(' ', 1)[1] if ' ' in action_text else action_text
        self.text_input.text = clean_text
        self.send_message(None)
        
    def send_message(self, instance):
        """Send user message and get response"""
        user_message = self.text_input.text.strip()
        if not user_message:
            return
            
        # Add user message
        self.add_message("You", user_message)
        self.text_input.text = ""
        
        # Show typing indicator
        self.add_message("Assistant", "Typing...")
        
        # Get response in background thread
        threading.Thread(
            target=self.get_response_async,
            args=(user_message,),
            daemon=True
        ).start()
        
    def get_response_async(self, message):
        """Get response from chatbot asynchronously"""
        try:
            if self.chatbot and BACKEND_AVAILABLE:
                response = self.chatbot.get_response(message)
            else:
                response = self.get_demo_response(message)
                
            # Remove typing indicator and add response
            Clock.schedule_once(
                lambda dt: self.replace_last_message("Assistant", response),
                0
            )
            
        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            Clock.schedule_once(
                lambda dt: self.replace_last_message("Assistant", error_msg),
                0
            )
            
    def replace_last_message(self, sender, message):
        """Replace the last message (used to replace typing indicator)"""
        if self.chat_layout.children:
            # Remove typing indicator
            self.chat_layout.remove_widget(self.chat_layout.children[0])
            
        # Add actual response
        self.add_message(sender, message)
        
    def get_demo_response(self, message):
        """Generate demo responses when backend isn't available"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['budget', 'budgeting']):
            return ("Creating a budget is essential! Here's a simple approach:\n\n"
                   "1. Track income and expenses\n"
                   "2. Use 50/30/20 rule\n"
                   "3. Start with essentials\n"
                   "4. Set realistic goals\n\n"
                   "Need help with a specific category?")
                   
        elif any(word in message_lower for word in ['invest', 'investment']):
            return ("Great investing question! For beginners:\n\n"
                   "1. Build emergency fund first\n"
                   "2. Consider index funds\n"
                   "3. Use 401(k) matching\n"
                   "4. Diversify portfolio\n"
                   "5. Think long-term\n\n"
                   "Want specific investment advice?")
                   
        elif any(word in message_lower for word in ['debt', 'loan']):
            return ("Debt management strategies:\n\n"
                   "1. List all debts\n"
                   "2. Pay minimums first\n"
                   "3. Use avalanche/snowball method\n"
                   "4. Avoid new debt\n\n"
                   "Need help prioritizing debts?")
                   
        else:
            return ("I'm here to help with your finances!\n\n"
                   "Try asking about:\n"
                   "💰 Budgeting tips\n"
                   "📈 Investment advice\n"
                   "💳 Debt strategies\n"
                   "🏠 Saving goals\n\n"
                   "What's your main financial concern?")


class FinanceChatbotApp(App):
    """Main Kivy application"""
    
    def build(self):
        """Build the application"""
        # Set window properties
        Window.clearcolor = (0.95, 0.95, 0.95, 1)
        Window.size = (400, 700)  # Mobile-like proportions
        
        # Create screen manager
        sm = ScreenManager()
        
        # Add chat screen
        chat_screen = ChatScreen(name='chat')
        sm.add_widget(chat_screen)
        
        return sm
        
    def on_start(self):
        """Called when the app starts"""
        print("🚀 Personal Finance Chatbot - Kivy Mobile Interface")
        print(f"🔧 Backend available: {BACKEND_AVAILABLE}")
        print(f"📱 Window size: {Window.size}")


def main():
    """Main function to run the Kivy app"""
    if not KIVY_AVAILABLE:
        print("❌ Kivy is not installed!")
        print("Install it with: pip install kivy")
        return
        
    print("🚀 Starting Kivy Mobile-Style Frontend...")
    app = FinanceChatbotApp()
    app.run()


if __name__ == "__main__":
    main()
