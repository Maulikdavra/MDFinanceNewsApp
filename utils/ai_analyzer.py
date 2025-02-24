import os
from openai import OpenAI
import json

class AIAnalyzer:
    def __init__(self):
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        self.client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
        self.model = "gpt-4o"

    def summarize_news(self, text):
        """
        Generate a concise summary of the news article
        """
        if not text:
            return "No content available to summarize."

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional news summarizer. Create a concise, clear summary of the following news article in 2-3 sentences."
                    },
                    {"role": "user", "content": text}
                ],
                max_tokens=150
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error generating summary: {str(e)}")

    def categorize_news(self, text):
        """
        Categorize news into Technology, Market, or Press Releases
        """
        if not text:
            return {"category": "Technology"}

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Categorize the following news title into one of these categories: Technology, Market, or Press Releases. Consider the content and context carefully. Respond in JSON format with a 'category' field."
                    },
                    {"role": "user", "content": text}
                ],
                response_format={"type": "json_object"}
            )
            result = json.loads(response.choices[0].message.content)
            if 'category' not in result:
                return {"category": "Technology"}
            return result
        except Exception as e:
            return {"category": "Technology"}  # Default category on error

    def analyze_sentiment(self, text):
        """
        Analyze the sentiment of the news article
        """
        if not text:
            return {"rating": 3, "confidence": 0.5}

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Analyze the sentiment of the news article and provide a rating from 1 to 5 stars (1 being very negative, 5 being very positive) and a confidence score between 0 and 1. Consider the overall tone, facts presented, and implications. Respond with JSON in this format: {'rating': number, 'confidence': number}"
                    },
                    {"role": "user", "content": text}
                ],
                response_format={"type": "json_object"}
            )
            result = json.loads(response.choices[0].message.content)
            return {
                "rating": max(1, min(5, round(result.get("rating", 3)))),
                "confidence": max(0, min(1, result.get("confidence", 0.5)))
            }
        except Exception as e:
            return {"rating": 3, "confidence": 0.5}  # Default values on error