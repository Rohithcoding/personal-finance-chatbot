# 🐍 Python Frontend Collection

This directory contains multiple Python-based frontend interfaces for the Personal Finance Chatbot. Choose the one that best fits your needs!

## 🎯 Available Python Frontends

### 1. 🖥️ Tkinter Desktop App (`tkinter_app.py`)
**Modern desktop application with native OS integration**

**Features:**
- Professional desktop GUI with modern styling
- Real-time chat with smooth animations
- Financial amount highlighting
- API status indicators
- Quick action buttons
- Threaded responses (non-blocking UI)
- Cross-platform (Windows, macOS, Linux)

**Requirements:**
- Python 3.6+ (Tkinter included)
- No additional dependencies needed

**Run:**
```bash
python frontend/tkinter_app.py
```

---

### 2. 🌐 FastAPI Web App (`fastapi_frontend.py`)
**Modern web interface built entirely in Python**

**Features:**
- Beautiful responsive web design
- Built-in HTML template generation
- RESTful API endpoints
- Session management
- Mobile-responsive design
- Auto-generated documentation
- Production-ready

**Requirements:**
```bash
pip install fastapi uvicorn jinja2
```

**Run:**
```bash
python frontend/fastapi_frontend.py
# Visit: http://localhost:8000
```

**API Endpoints:**
- `GET /` - Main chat interface
- `POST /chat` - Send messages
- `GET /api/status` - API status
- `GET /clear` - Clear chat history

---

### 3. 📱 Kivy Mobile App (`kivy_mobile_app.py`)
**Mobile-style interface for cross-platform deployment**

**Features:**
- Mobile-like UI design
- Touch-friendly interface
- Message bubbles
- Smooth scrolling
- Cross-platform mobile deployment
- Customizable themes

**Requirements:**
```bash
pip install kivy
```

**Run:**
```bash
python frontend/kivy_mobile_app.py
```

## 🚀 Quick Start Guide

### Option 1: Desktop Experience (Recommended for local use)
```bash
# No installation needed - uses built-in Tkinter
python frontend/tkinter_app.py
```

### Option 2: Web Experience (Recommended for sharing)
```bash
# Install web dependencies
pip install fastapi uvicorn jinja2

# Run web server
python frontend/fastapi_frontend.py

# Open browser to http://localhost:8000
```

### Option 3: Mobile Experience
```bash
# Install mobile dependencies
pip install kivy

# Run mobile-style app
python frontend/kivy_mobile_app.py
```

## 🔧 Configuration

All frontends automatically detect and use your backend configuration:

1. **With APIs configured**: Full functionality with OpenAI and Google Cloud
2. **Demo mode**: Works without API keys for testing

### Environment Variables
Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_APPLICATION_CREDENTIALS=path/to/google-cloud-key.json
```

## 🎨 Features Comparison

| Feature | Tkinter | FastAPI | Kivy |
|---------|---------|---------|------|
| **Platform** | Desktop | Web | Mobile/Desktop |
| **Installation** | ✅ Built-in | 📦 Pip install | 📦 Pip install |
| **UI Style** | Native OS | Modern Web | Mobile-like |
| **Deployment** | Executable | Web Server | App Store |
| **Responsive** | Window resize | ✅ Yes | Touch-friendly |
| **Offline** | ✅ Yes | Server needed | ✅ Yes |

## 🛠️ Development

### Adding New Features
Each frontend is modular and extensible:

1. **Tkinter**: Modify widgets in `ModernChatGUI` class
2. **FastAPI**: Add routes and update templates
3. **Kivy**: Create new screens and widgets

### Custom Styling
- **Tkinter**: Modify `setup_styles()` method
- **FastAPI**: Edit CSS in template generation
- **Kivy**: Update canvas instructions and colors

## 📱 Mobile Deployment

### Kivy Mobile App
Deploy to iOS/Android using buildozer:

```bash
# Install buildozer
pip install buildozer

# Initialize buildozer config
buildozer init

# Build Android APK
buildozer android debug
```

### Web App Mobile
The FastAPI frontend is already mobile-responsive and works great on mobile browsers.

## 🔍 Troubleshooting

### Tkinter Issues
```bash
# macOS: Install tkinter
brew install python-tk

# Ubuntu/Debian: Install tkinter
sudo apt-get install python3-tk

# Windows: Usually included with Python
```

### FastAPI Issues
```bash
# Install dependencies
pip install fastapi uvicorn jinja2 python-multipart

# Run with custom port
python frontend/fastapi_frontend.py --port 8080
```

### Kivy Issues
```bash
# Install dependencies
pip install kivy[base,media,dev]

# macOS additional deps
brew install pkg-config sdl2 sdl2_image sdl2_ttf sdl2_mixer gstreamer
```

## 🎯 Which Frontend to Choose?

### Choose **Tkinter** if:
- You want a native desktop experience
- No additional installations needed
- Building standalone executables
- Users prefer desktop applications

### Choose **FastAPI** if:
- You need web-based deployment
- Multiple users will access it
- You want modern web UI
- Planning to deploy on cloud platforms

### Choose **Kivy** if:
- Building mobile applications
- Need touch-friendly interface
- Want to distribute via app stores
- Cross-platform mobile deployment

## 📚 API Integration

All frontends seamlessly integrate with the backend:

```python
# Backend integration example
from backend.main import PersonalFinanceChatbot
from backend.utils import extract_amounts, format_currency

# Initialize chatbot
chatbot = PersonalFinanceChatbot()

# Get response
response = chatbot.get_response("How should I budget $3000?")
```

## 🚀 Production Deployment

### FastAPI Web Deployment
```bash
# Install production server
pip install gunicorn

# Run with gunicorn
gunicorn frontend.fastapi_frontend:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Desktop App Distribution
```bash
# Create standalone executable
pip install pyinstaller

# Build Tkinter app
pyinstaller --onefile --windowed frontend/tkinter_app.py
```

Choose the frontend that best matches your deployment needs and user preferences! 🎉
