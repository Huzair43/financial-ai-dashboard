from src.data_loader import FinancialDataLoader

def test_news_api():
    loader = FinancialDataLoader("TSLA")
    news = loader.get_stock_news()
    
    if news:
        print(f"Succès ! Récupéré {len(news)} news pour Tesla.")
        print(f"Titre de la première : {news[0]['title']}")
        print(f"Sentiment API : {news[0]['api_sentiment']}")
    else:
        print("Échec de la récupération des news.")

if __name__ == "__main__":
    test_news_api()