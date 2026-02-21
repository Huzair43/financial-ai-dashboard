from src.data_loader import FinancialDataLoader
from src.sentiment_analyzer import SentimentAnalyzer
from src.logger import PredictionLogger

def run_demo(ticker="TSLA", nb_articles=5):
    print(f"\n--- Analyse CLI pour : {ticker} ---")

    # Initialisation des outils
    loader = FinancialDataLoader(ticker)
    ia = SentimentAnalyzer()
    logger = PredictionLogger()

    # Récupération des news
    news_items = loader.get_stock_news(ticker)
    if not news_items:
        print("Aucune news trouvée.")
        return

    # Analyse des N premières news
    print(f"\n{'TITRE':<50} | {'API SENTIMENT':<15} | {'IA SENTIMENT'}")
    print("-" * 85)
    for news in news_items[:nb_articles]:
        titre = news['title']
        ia_result = ia.analyze(titre)

        # Log dans la DB
        logger.log(
            ticker=ticker,
            text=titre,
            api_sentiment=news['api_sentiment'],
            api_score=news['api_score'],
            model_label=ia_result['label'],
            model_score=ia_result['score'],
            model_version=ia.version
        )

        # Affichage CLI
        short_title = (titre[:47] + '..') if len(titre) > 47 else titre
        print(f"{short_title:<50} | {news['api_sentiment']:<15} | {ia_result['label']} ({ia_result['score']})")

if __name__ == "__main__":
    # Exemple : analyse de TSLA
    run_demo(ticker="TSLA", nb_articles=5)