# Personal Finance Chatbot 💰

A Streamlit-based personal finance chatbot that provides financial advice and analysis using OpenAI GPT and Google Cloud Natural Language API.

## Features

- Interactive chat interface for financial advice
- Sentiment analysis of financial queries
- Financial calculations (compound interest, loan payments, etc.)
- Expense categorization
- OpenAI GPT integration for intelligent responses
- Google Cloud NLU for sentiment analysis

## Project Structure

```
personal-finance-chatbot/
├── streamlit_app.py          # Streamlit web application
├── api_server.py            # Flask API server for frontend
├── requirements.txt          # Python dependencies
├── frontend/                # Modern web frontend
│   ├── index.html           # HTML structure
│   ├── styles.css           # CSS styling
│   ├── script.js            # JavaScript functionality
│   └── README.md           # Frontend documentation
├── backend/                  # Backend modules
│   ├── main.py              # Main chatbot logic
│   ├── openai_api.py        # OpenAI API integration
│   ├── google_nlu_api.py    # Google Cloud NLU integration
│   └── utils.py             # Utility functions
├── .env.example             # Environment variables template
└── README.md               # This file
```

## Setup

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/Rohithcoding/personal-finance-chatbot.git
cd personal-finance-chatbot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. Run the application:

**Option A: Streamlit Interface (Recommended for development)**
```bash
streamlit run streamlit_app.py
```

**Option B: Modern Web Frontend (Recommended for production)**
```bash
python api_server.py
```
Visit: http://localhost:8000

### Environment Variables

Create a `.env` file with the following variables:

```
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_APPLICATION_CREDENTIALS=path_to_your_google_cloud_key.json
```

## Deployment Options

### Option 1: Deploy on Render (Recommended)

1. **Fork this repository** to your GitHub account

2. **Sign up for Render** at [render.com](https://render.com)

3. **Connect your GitHub account** to Render

4. **Create a new Web Service**:
   - Click "New +" → "Web Service"
   - Choose "Build and deploy from a Git repository"
   - Select your forked repository
   - Configure the service:
     - **Name**: `personal-finance-chatbot`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true`
     - **Plan**: Free (or choose paid for better performance)

5. **Add Environment Variables** in Render dashboard:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `GOOGLE_APPLICATION_CREDENTIALS`: For local development, use the path to your JSON file. For Render, you'll need to base64 encode the JSON content and set it as the value.

6. **Deploy**: Click "Create Web Service"

### Option 2: Deploy with Docker

```bash
# Build the Docker image
docker build -t personal-finance-chatbot .

# Run the container
docker run -p 8501:8501 \
  -e OPENAI_API_KEY=your_key_here \
  -e GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json \
  personal-finance-chatbot
```

### Option 3: Deploy on Streamlit Cloud

1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Deploy your fork
5. Add secrets in Streamlit Cloud dashboard

## API Keys Required

### OpenAI API
1. Visit [OpenAI API](https://platform.openai.com/api-keys)
2. Create an account and generate an API key
3. Add the key to your environment variables

### Google Cloud Natural Language API
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable the Natural Language API
4. Create a service account and download the JSON key file
5. Set the path to the JSON file in your environment variables

## Usage

1. Open the application in your browser
2. Start chatting with the finance bot
3. Ask questions about:
   - Investment advice
   - Loan calculations
   - Budgeting tips
   - Financial planning
   - Expense tracking

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details.

## 🐍 Python Frontend Collection

This project now includes **multiple Python-based frontends** in addition to the Streamlit interface:

### Available Interfaces:

#### 1. 🖥️ Tkinter Desktop App
**Professional native desktop application**
```bash
python frontend/tkinter_app.py
```
- Modern GUI with native OS integration
- Real-time chat with animations
- Financial amount highlighting
- No additional dependencies (uses built-in Tkinter)

#### 2. 🌐 FastAPI Web App  
**Modern web interface built entirely in Python**
```bash
pip install fastapi uvicorn jinja2
python frontend/fastapi_frontend.py
# Visit: http://localhost:8000
```
- Beautiful responsive web design
- RESTful API endpoints
- Production-ready deployment
- Auto-generated documentation

#### 3. 📱 Kivy Mobile App
**Mobile-style interface for cross-platform deployment**
```bash
pip install kivy
python frontend/kivy_mobile_app.py
```
- Touch-friendly mobile-like UI
- Cross-platform mobile deployment
- Message bubbles and smooth scrolling
- Can be compiled to mobile apps

#### 4. 🎨 Streamlit Interface (Original)
**Data science focused interface**
```bash
streamlit run streamlit_app.py
```
- Great for prototyping and demos
- Built-in widgets and charts
- Easy deployment on Streamlit Cloud

### Quick Comparison:

| Interface | Best For | Installation | Deployment |
|-----------|----------|-------------|------------|
| **Tkinter** | Desktop users | ✅ Built-in | Executable |
| **FastAPI** | Web deployment | 📦 pip install | Web server |
| **Kivy** | Mobile apps | 📦 pip install | App stores |
| **Streamlit** | Prototyping | 📦 pip install | Cloud hosting |

Choose the interface that best fits your needs! All frontends use the same powerful backend with OpenAI and Google Cloud integration.

📚 **Detailed documentation**: See `frontend/README.md` for comprehensive setup and usage instructions.
