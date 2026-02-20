from transformers import pipeline

class SentimentAnalyzer:
    def __init__(self):
        print("--- Chargement de FinBERT (Modèle IA spécialisé finance) ---")
        # On utilise le modèle ProsusAI/finbert, la référence en NLP financier
        self.analyzer = pipeline("sentiment-analysis", model="ProsusAI/finbert")

    def analyze(self, text):
        if not text or len(text.strip()) == 0:
            return {"label": "Neutral", "score": 0.0}
        
        # Le modèle ne peut lire que 512 tokens max
        result = self.analyzer(text[:512])[0]
        return {
            "label": result['label'],
            "score": round(result['score'], 4)
        }