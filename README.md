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
├── streamlit_app.py          # Main Streamlit application
├── requirements.txt          # Python dependencies
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
```bash
streamlit run streamlit_app.py
```

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
