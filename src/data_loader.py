import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup

class FinancialDataLoader:
    """Classe pour extraire les données boursières et financières."""
    
    def __init__(self, ticker: str):
        self.ticker_symbol = ticker
        self.stock = yf.Ticker(ticker)

    def get_stock_history(self, period="max"):
        """Récupère l'historique des prix avec gestion d'erreur."""
        try:
            data = self.stock.history(period=period)
            if data.empty:
                print(f"Warning: No data found for {self.ticker_symbol}")
            return data.reset_index()
        except Exception as e:
            print(f"Erreur lors de l'appel à yfinance: {e}")
            # En cas d'erreur, on retourne un DataFrame vide au lieu de faire planter le programme
            return pd.DataFrame()

    def get_revenue_data(self, url: str):
        """Scrape les revenus depuis une page HTML (ex: Macrotrends)."""
        headers = {"User-Agent": "Mozilla/5.0"}
        html_data = requests.get(url, headers=headers).text
        soup = BeautifulSoup(html_data, 'html.parser')
        
        # Logique simplifiée de ton notebook
        tables = soup.find_all("table")
        # On cherche la table des revenus annuels (généralement la 2ème)
        table_index = 1 
        
        revenue_df = pd.read_html(str(tables[table_index]))[0]
        revenue_df.columns = ["Date", "Revenue"]
        
        # Nettoyage des données (enlever les $ et les virgules)
        revenue_df["Revenue"] = revenue_df['Revenue'].replace({'\$': '', ',': ''}, regex=True)
        revenue_df.dropna(inplace=True)
        revenue_df = revenue_df[revenue_df['Revenue'] != ""]
        
        return revenue_df