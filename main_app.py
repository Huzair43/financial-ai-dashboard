from src.data_loader import FinancialDataLoader
from src.sentiment_analyzer import SentimentAnalyzer

def run_demo(ticker="TSLA"):
    print(f"\n--- Analyse en cours pour : {ticker} ---")
    
    # 1. Récupération des données via ton API Alpha Vantage
    loader = FinancialDataLoader(ticker)
    news_items = loader.get_stock_news()
    
    if not news_items:
        print("Aucune news trouvée.")
        return

    # 2. Initialisation de ton IA
    ia = SentimentAnalyzer()
    
    print(f"\n{'TITRE':<50} | {'API SENTIMENT':<15} | {'IA SENTIMENT'}")
    print("-" * 85)

    # 3. Comparaison en temps réel
    for news in news_items[:5]: # On analyse les 5 premières
        titre = news['title']
        ia_result = ia.analyze(titre)
        
        # Formatage propre pour l'affichage
        short_title = (titre[:47] + '..') if len(titre) > 47 else titre
        print(f"{short_title:<50} | {news['api_sentiment']:<15} | {ia_result['label']} ({ia_result['score']})")

if __name__ == "__main__":
    run_demo()