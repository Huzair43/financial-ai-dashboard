import os
import requests
import pandas as pd
from dotenv import load_dotenv

# Charger la clé API depuis le fichier .env
load_dotenv()
print(f"DEBUG: Clé récupérée -> {os.getenv('ALPHA_VANTAGE_KEY')}") # Ajoute cette ligne !

class FinancialDataLoader:
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.api_key = os.getenv("ALPHA_VANTAGE_KEY")
        self.base_url = "https://www.alphavantage.co/query"

    def get_stock_news(self):
        params = {
            "function": "NEWS_SENTIMENT",
            "tickers": self.ticker,
            "apikey": self.api_key,
            "sort": "LATEST",
            "limit": 5
        }
        
        response = requests.get(self.base_url, params=params)
        data = response.json()
        
        # AJOUTE CETTE LIGNE POUR DEBUGGER :
        print("DEBUG API RESPONSE:", data)
        
        if "feed" not in data:
            return []
            
        news_list = []
        for item in data["feed"]:
            news_list.append({
                "title": item["title"],
                "summary": item["summary"],
                "url": item["url"],
                "api_sentiment": item["overall_sentiment_label"],
                "api_score": item["overall_sentiment_score"]
            })
            
        return news_list