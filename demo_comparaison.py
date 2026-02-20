from src.data_loader import FinancialDataLoader
from src.sentiment_analyzer import SentimentAnalyzer

def test_comparaison():
    # On initialise nos deux outils
    loader = FinancialDataLoader("TSLA")
    ia = SentimentAnalyzer()
    
    # On récupère les news
    news_list = loader.get_stock_news()
    
    if news_list:
        # On prend la news la plus récente
        news = news_list[0]
        titre = news['title']
        
        # L'IA fait son analyse
        resultat_ia = ia.analyze(titre)
        
        print("\n" + "="*60)
        print(f"VALEUR ANALYSÉE : {titre}")
        print("="*60)
        print(f"🤖 ANALYSE API  : {news['api_sentiment']} (Score: {news['api_score']})")
        print(f"🧠 ANALYSE TON IA: {resultat_ia['label']} (Confiance: {resultat_ia['score']})")
        print("="*60)
        
        # Petit diagnostic de l'ingénieur
        if news['api_sentiment'].lower() == resultat_ia['label'].lower():
            print("✅ Résultat : Consensus (L'IA et l'API sont d'accord).")
        else:
            print("⚠️ Résultat : Divergence ! Ton IA voit une nuance que l'API ignore.")

if __name__ == "__main__":
    test_comparaison()