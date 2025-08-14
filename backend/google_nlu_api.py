"""
Google Cloud Natural Language API integration
"""

import os
from typing import Dict

try:
    from google.cloud import language_v1
    GOOGLE_CLOUD_AVAILABLE = True
except ImportError:
    GOOGLE_CLOUD_AVAILABLE = False

class GoogleNLUHandler:
    """Handle Google Cloud Natural Language API interactions"""
    
    def __init__(self):
        self.client = None
        if GOOGLE_CLOUD_AVAILABLE and os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
            try:
                self.client = language_v1.LanguageServiceClient()
            except Exception as e:
                print(f"Failed to initialize Google NLU client: {e}")
    
    def analyze_sentiment(self, text: str) -> Dict:
        """Analyze sentiment of the given text"""
        if not self.client:
            return {
                "sentiment": "unknown",
                "score": 0.0,
                "magnitude": 0.0,
                "error": "Google Cloud NLU not available"
            }
        
        try:
            document = language_v1.Document(
                content=text,
                type_=language_v1.Document.Type.PLAIN_TEXT
            )
            
            response = self.client.analyze_sentiment(
                request={"document": document}
            )
            
            sentiment = response.document_sentiment
            
            return {
                "sentiment": self._get_sentiment_label(sentiment.score),
                "score": sentiment.score,
                "magnitude": sentiment.magnitude
            }
            
        except Exception as e:
            return {
                "sentiment": "error",
                "score": 0.0,
                "magnitude": 0.0,
                "error": str(e)
            }
    
    def _get_sentiment_label(self, score: float) -> str:
        """Convert sentiment score to label"""
        if score > 0.25:
            return "positive"
        elif score < -0.25:
            return "negative"
        else:
            return "neutral"
