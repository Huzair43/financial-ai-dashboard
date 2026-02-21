from src.logger import PredictionLogger

def test_logger():
    logger = PredictionLogger()
    logger.log(
        ticker="TSLA",
        text="Test news",
        api_sentiment="neutral",
        api_score=0.5,
        model_label="neutral",
        model_score=0.7,
        model_version="finbert-v1"
    )
    print("✅ Logger fonctionne")