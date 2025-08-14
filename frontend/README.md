# Personal Finance Chatbot - Frontend

A modern, responsive web interface for the Personal Finance Chatbot built with HTML, CSS, and JavaScript.

## Features

- 🎨 **Modern UI Design**: Clean, professional interface with gradient backgrounds
- 📱 **Responsive Layout**: Works seamlessly on desktop, tablet, and mobile devices  
- 💬 **Real-time Chat**: Interactive chat interface with typing indicators
- 🤖 **AI Integration**: Connects to OpenAI and Google Cloud APIs via backend
- 📊 **Financial Analysis**: Automatic amount extraction and sentiment analysis
- ⚡ **Quick Actions**: Pre-defined financial questions for easy access
- 🔄 **Real-time Status**: Live API connection status indicators

## File Structure

```
frontend/
├── index.html          # Main HTML structure
├── styles.css          # CSS styling and responsive design
├── script.js           # JavaScript functionality
└── README.md          # This documentation
```

## Getting Started

### Option 1: Run with Flask API Server (Recommended)

From the project root directory:

```bash
# Install dependencies
pip install -r requirements.txt

# Start the Flask API server (serves both API and frontend)
python api_server.py
```

Visit: http://localhost:8000

### Option 2: Serve Static Files

You can serve the frontend files directly using any web server:

```bash
# Using Python's built-in server
cd frontend
python -m http.server 8080

# Using Node.js (if you have it installed)
npx serve .

# Using PHP (if you have it installed)  
php -S localhost:8080
```

Note: When serving static files, the backend API integration won't work. The frontend will run in demo mode with fallback responses.

## Features in Detail

### Chat Interface
- Real-time messaging with smooth animations
- User and assistant message differentiation
- Automatic scrolling to latest messages
- Loading indicators during processing

### Financial Analysis
- **Amount Detection**: Automatically highlights monetary amounts in messages
- **Sentiment Analysis**: Shows emotional tone of financial queries
- **Quick Actions**: One-click buttons for common financial questions

### Responsive Design
- Mobile-first approach
- Sidebar collapses on mobile devices
- Touch-friendly interface elements
- Optimized for all screen sizes

## Customization

### Styling
Edit `styles.css` to customize:
- Color scheme (gradients, backgrounds)
- Typography (fonts, sizes)
- Layout (spacing, sizing)
- Animations and transitions

### Functionality
Edit `script.js` to customize:
- API endpoints
- Message processing
- Response formatting
- Quick action buttons

### Content
Edit `index.html` to customize:
- Page title and meta information
- Sidebar content
- Feature descriptions
- Quick action buttons

## API Integration

The frontend is designed to work with the Flask API server (`api_server.py`) which provides:

- `/health` - API status check
- `/chat` - Chat message processing
- Static file serving

When the API is not available, the frontend gracefully falls back to demo mode with predefined responses.

## Browser Support

- Chrome 70+
- Firefox 65+
- Safari 12+
- Edge 79+

## Dependencies

- Font Awesome 6.0 (icons)
- Inter font (typography)
- Modern CSS features (Grid, Flexbox, CSS Variables)
- ES6+ JavaScript features

All external dependencies are loaded via CDN, so no additional installation is required.

## Development

For development with hot-reload and debugging:

```bash
# Set Flask to development mode
export FLASK_ENV=development

# Run the API server
python api_server.py
```

This enables:
- Auto-restart on code changes
- Detailed error messages
- Debug logging in browser console
