import os
from openai import OpenAI
import json

class AIAnalyzer:
    def __init__(self):
        # Initialize OpenAI client with error handling
        api_key = os.environ.get('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OpenAI API key not found in environment variables")
        self.client = OpenAI(api_key=api_key)
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        self.model = "gpt-4o"

    def summarize_news(self, text):
        """
        Generate a concise summary of the news article
        """
        if not text or not isinstance(text, str):
            return "No content available to summarize."

        try:
            # Clean and prepare the text
            cleaned_text = text.strip()
            if not cleaned_text:
                return "No content available to summarize."

            # Make API call with better error handling
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """You are a professional news summarizer. Create a concise, informative 
                        summary of the following news article in 2-3 sentences. Focus on the key points 
                        and maintain factual accuracy."""
                    },
                    {"role": "user", "content": cleaned_text}
                ],
                max_tokens=150,
                temperature=0.7
            )

            # Verify response structure
            if not response.choices or not response.choices[0].message:
                return "Error: Unable to generate summary"

            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"Error in summarize_news: {str(e)}")  # Debug log
            return "Unable to generate summary at this time."

    def categorize_news(self, text):
        """
        Categorize news into Technology, Market, or Press Releases
        """
        if not text or not isinstance(text, str):
            return {"category": "Technology"}

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """Categorize the following news title into one of these categories: 
                        Technology, Market, or Press Releases. Consider the content and context carefully. 
                        Respond in JSON format with a 'category' field."""
                    },
                    {"role": "user", "content": text.strip()}
                ],
                response_format={"type": "json_object"}
            )

            result = json.loads(response.choices[0].message.content)
            if 'category' not in result:
                return {"category": "Technology"}
            return result

        except Exception as e:
            print(f"Error in categorize_news: {str(e)}")  # Debug log
            return {"category": "Technology"}

    def analyze_sentiment(self, text):
        """
        Analyze the sentiment of the news article
        """
        if not text or not isinstance(text, str):
            return {"rating": 3, "confidence": 0.5}

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """Analyze the sentiment of the news article and provide a rating 
                        from 1 to 5 stars (1 being very negative, 5 being very positive) and a 
                        confidence score between 0 and 1. Consider the overall tone, facts presented, 
                        and implications. Respond with JSON in this format: 
                        {'rating': number, 'confidence': number}"""
                    },
                    {"role": "user", "content": text.strip()}
                ],
                response_format={"type": "json_object"}
            )

            result = json.loads(response.choices[0].message.content)
            return {
                "rating": max(1, min(5, round(result.get("rating", 3)))),
                "confidence": max(0, min(1, result.get("confidence", 0.5)))
            }

        except Exception as e:
            print(f"Error in analyze_sentiment: {str(e)}")  # Debug log
            return {"rating": 3, "confidence": 0.5}