// Personal Finance Chatbot - Frontend JavaScript

class FinanceChatbot {
    constructor() {
        this.apiBaseUrl = 'http://localhost:8000'; // Backend API URL
        this.chatMessages = document.getElementById('chat-messages');
        this.userInput = document.getElementById('user-input');
        this.sendBtn = document.getElementById('send-btn');
        this.chatForm = document.getElementById('chat-form');
        this.loadingModal = document.getElementById('loading-modal');
        
        this.initializeEventListeners();
        this.checkApiStatus();
        this.focusInput();
    }

    initializeEventListeners() {
        // Form submission
        this.chatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.sendMessage();
        });

        // Enter key in input
        this.userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Auto-resize input
        this.userInput.addEventListener('input', () => {
            this.userInput.style.height = 'auto';
            this.userInput.style.height = this.userInput.scrollHeight + 'px';
        });
    }

    focusInput() {
        setTimeout(() => {
            this.userInput.focus();
        }, 100);
    }

    async checkApiStatus() {
        try {
            // Simulate API status check (replace with actual endpoint)
            const response = await fetch(`${this.apiBaseUrl}/health`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                const data = await response.json();
                this.updateApiStatus('openai', data.openai_status);
                this.updateApiStatus('google', data.google_status);
            }
        } catch (error) {
            console.log('API not available, running in demo mode');
            // Demo mode - show not connected status
            this.updateApiStatus('openai', false);
            this.updateApiStatus('google', false);
        }
    }

    updateApiStatus(service, isConnected) {
        const statusElement = document.getElementById(`${service}-status`);
        if (isConnected) {
            statusElement.textContent = '✅ Connected';
            statusElement.style.color = '#27ae60';
        } else {
            statusElement.textContent = '❌ Not Connected';
            statusElement.style.color = '#e74c3c';
        }
    }

    async sendMessage() {
        const message = this.userInput.value.trim();
        if (!message) return;

        // Disable input and show loading
        this.setLoading(true);
        
        // Add user message to chat
        this.addMessage(message, 'user');
        
        // Clear input
        this.userInput.value = '';
        this.userInput.style.height = 'auto';

        try {
            // Send to backend API
            const response = await this.callAPI(message);
            
            // Add response to chat
            this.addMessage(response.text, 'assistant', response.metadata);
            
        } catch (error) {
            console.error('Error:', error);
            // Fallback response
            const fallbackResponse = this.generateFallbackResponse(message);
            this.addMessage(fallbackResponse, 'assistant');
        } finally {
            this.setLoading(false);
            this.focusInput();
        }
    }

    async callAPI(message) {
        // Try to call the actual API first
        try {
            const response = await fetch(`${this.apiBaseUrl}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            });

            if (response.ok) {
                return await response.json();
            }
        } catch (error) {
            console.log('API call failed, using fallback');
        }

        // Fallback to demo responses
        return {
            text: this.generateFallbackResponse(message),
            metadata: this.analyzeMessage(message)
        };
    }

    generateFallbackResponse(message) {
        const lowerMessage = message.toLowerCase();
        
        // Financial keywords and responses
        const responses = {
            investment: "Great question about investing! Here are some key principles: 1) Start early to benefit from compound interest, 2) Diversify your portfolio across different asset classes, 3) Consider low-cost index funds for beginners, 4) Only invest money you won't need for at least 5 years. Would you like specific advice based on your risk tolerance?",
            
            budget: "Creating a budget is essential for financial health! Try the 50/30/20 rule: 50% for needs (rent, utilities, groceries), 30% for wants (entertainment, dining out), and 20% for savings and debt repayment. Track your expenses for a month to see where your money goes, then adjust accordingly.",
            
            loan: "For loan calculations, the key factors are: principal amount, interest rate, and loan term. For example, a $10,000 loan at 5% annual interest for 5 years would have monthly payments of approximately $188.71. Would you like me to help calculate payments for a specific loan scenario?",
            
            save: "Smart saving strategies include: 1) Pay yourself first - save before spending, 2) Automate transfers to savings, 3) Build an emergency fund of 3-6 months expenses, 4) Take advantage of high-yield savings accounts, 5) Consider cutting unnecessary subscriptions and expenses.",
            
            debt: "For debt management: 1) List all debts with balances and interest rates, 2) Consider the debt snowball (pay minimums, extra to smallest) or avalanche method (extra to highest interest), 3) Avoid taking on new debt, 4) Consider debt consolidation if it lowers your interest rate.",
            
            retirement: "Retirement planning tips: 1) Start as early as possible, 2) Contribute enough to get your employer's 401(k) match, 3) Consider both traditional and Roth IRA options, 4) Aim to save 10-15% of your income, 5) Review and adjust your plan annually."
        };

        // Check for keywords and return appropriate response
        for (const [keyword, response] of Object.entries(responses)) {
            if (lowerMessage.includes(keyword)) {
                return response;
            }
        }

        // Default response
        return `I understand you're asking about: "${message}". While I'd love to provide personalized financial advice, I recommend consulting with a qualified financial advisor for your specific situation. However, I can help with general questions about budgeting, saving, investing basics, and financial calculations. What specific area would you like to explore?`;
    }

    analyzeMessage(message) {
        // Simple analysis for demo purposes
        const amounts = this.extractAmounts(message);
        const sentiment = this.analyzeSentiment(message);
        
        return {
            amounts: amounts,
            sentiment: sentiment
        };
    }

    extractAmounts(text) {
        const amountRegex = /\$?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)/g;
        const matches = [];
        let match;
        
        while ((match = amountRegex.exec(text)) !== null) {
            const amount = parseFloat(match[1].replace(/,/g, ''));
            if (amount > 0) {
                matches.push(amount);
            }
        }
        
        return matches;
    }

    analyzeSentiment(text) {
        // Simple keyword-based sentiment analysis
        const positiveWords = ['good', 'great', 'excellent', 'happy', 'excited', 'optimistic', 'confident'];
        const negativeWords = ['bad', 'terrible', 'worried', 'anxious', 'concerned', 'struggling', 'difficult'];
        
        const words = text.toLowerCase().split(/\s+/);
        let positiveCount = 0;
        let negativeCount = 0;
        
        words.forEach(word => {
            if (positiveWords.includes(word)) positiveCount++;
            if (negativeWords.includes(word)) negativeCount++;
        });
        
        if (positiveCount > negativeCount) return 'positive';
        if (negativeCount > positiveCount) return 'negative';
        return 'neutral';
    }

    addMessage(text, sender, metadata = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = sender === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
        
        const content = document.createElement('div');
        content.className = 'message-content';
        
        // Process text for amount highlighting
        let processedText = text;
        if (metadata && metadata.amounts && metadata.amounts.length > 0) {
            metadata.amounts.forEach(amount => {
                const formattedAmount = this.formatCurrency(amount);
                processedText = processedText.replace(
                    new RegExp(`\\$?${amount.toLocaleString()}`, 'g'),
                    `<span class="amount-highlight">${formattedAmount}</span>`
                );
            });
        }
        
        const textParagraph = document.createElement('p');
        textParagraph.innerHTML = processedText;
        content.appendChild(textParagraph);
        
        // Add sentiment info if available
        if (metadata && metadata.sentiment && metadata.sentiment !== 'neutral') {
            const sentimentDiv = document.createElement('div');
            sentimentDiv.className = 'sentiment';
            const emoji = metadata.sentiment === 'positive' ? '😊' : '😔';
            sentimentDiv.innerHTML = `${emoji} Sentiment: ${metadata.sentiment.charAt(0).toUpperCase() + metadata.sentiment.slice(1)}`;
            content.appendChild(sentimentDiv);
        }
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(content);
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }

    formatCurrency(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(amount);
    }

    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    setLoading(isLoading) {
        if (isLoading) {
            this.loadingModal.style.display = 'flex';
            this.sendBtn.disabled = true;
            this.userInput.disabled = true;
        } else {
            this.loadingModal.style.display = 'none';
            this.sendBtn.disabled = false;
            this.userInput.disabled = false;
        }
    }
}

// Quick message function for buttons
function sendQuickMessage(message) {
    const chatbot = window.financeChatbot;
    if (chatbot) {
        chatbot.userInput.value = message;
        chatbot.sendMessage();
    }
}

// Initialize chatbot when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.financeChatbot = new FinanceChatbot();
});

// Add some demo functionality for development
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    console.log('🤖 Personal Finance Chatbot loaded in development mode');
    console.log('Try asking questions about investing, budgeting, loans, or savings!');
}
