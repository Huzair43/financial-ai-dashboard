from src.data_loader import FinancialDataLoader
from src.sentiment_analyzer import SentimentAnalyzer
from src.logger import PredictionLogger

def test_comparaison(ticker="TSLA"):
    print(f"\n--- Comparaison API vs IA pour : {ticker} ---")

    # Initialisation
    loader = FinancialDataLoader(ticker)
    ia = SentimentAnalyzer()
    logger = PredictionLogger()

    # Récupération des news
    news_list = loader.get_stock_news(ticker)
    if not news_list:
        print("Aucune news trouvée.")
        return

    # On prend la news la plus récente
    news = news_list[0]
    titre = news['title']

    # Analyse IA
    resultat_ia = ia.analyze(titre)

    # Log dans la DB
    logger.log(
        ticker=ticker,
        text=titre,
        api_sentiment=news['api_sentiment'],
        api_score=news['api_score'],
        model_label=resultat_ia['label'],
        model_score=resultat_ia['score'],
        model_version=ia.version
    )

    # Affichage CLI
    print("\n" + "="*60)
    print(f"VALEUR ANALYSÉE : {titre}")
    print("="*60)
    print(f"🤖 ANALYSE API  : {news['api_sentiment']} (Score: {news['api_score']})")
    print(f"🧠 ANALYSE IA   : {resultat_ia['label']} (Confiance: {resultat_ia['score']})")
    print("="*60)

    # Diagnostic rapide
    if news['api_sentiment'].lower() == resultat_ia['label'].lower():
        print("✅ Résultat : Consensus (L'IA et l'API sont d'accord).")
    else:
        print("⚠️ Résultat : Divergence détectée !")

if __name__ == "__main__":
    test_comparaison(ticker="TSLA")