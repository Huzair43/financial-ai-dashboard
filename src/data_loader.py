import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

class FinancialDataLoader:
    def __init__(self, ticker: str):
        self.ticker = ticker.upper()
        self.base_url = "https://www.alphavantage.co/query"
        self.api_key = self._get_api_key()

    def _get_api_key(self):
        """Récupération sécurisée de la clé API"""
        try:
            if "ALPHA_VANTAGE_KEY" in st.secrets:
                return st.secrets["ALPHA_VANTAGE_KEY"]
        except:
            pass
        return os.getenv("ALPHA_VANTAGE_KEY")

    @st.cache_data(ttl=3600)
    def get_stock_news(_self, ticker_to_fetch: str):
        """
        Le paramètre ticker_to_fetch est crucial ici pour que le cache 
        se mette à jour quand on change de ticker.
        """
        if not _self.api_key:
            return None

        params = {
            "function": "NEWS_SENTIMENT",
            "tickers": ticker_to_fetch,
            "apikey": _self.api_key,
            "sort": "LATEST",
            "limit": 10
        }
        
        try:
            response = requests.get(_self.base_url, params=params)
            data = response.json()
            
            if "Note" in data:
                st.warning("⚠️ Limite d'API Alpha Vantage atteinte.")
                return []
                
            if "feed" not in data:
                return []
                
            return [{
                "title": item["title"],
                "summary": item["summary"],
                "url": item["url"],
                "api_sentiment": item["overall_sentiment_label"],
                "api_score": item["overall_sentiment_score"]
            } for item in data["feed"]]
        except Exception:
            return []