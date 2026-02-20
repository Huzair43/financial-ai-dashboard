import streamlit as st
from src.data_loader import FinancialDataLoader
from src.sentiment_analyzer import SentimentAnalyzer
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Financial AI Dashboard", layout="wide")

st.title("📊 Financial AI Sentiment Dashboard")
st.sidebar.header("Configuration")

# 1. Sélection du Ticker
ticker = st.sidebar.text_input("Entrez un Ticker (ex: TSLA, AAPL, AMZN)", value="TSLA")

# 2. Initialisation des outils (on utilise @st.cache_resource pour ne pas recharger l'IA à chaque clic)
@st.cache_resource
def load_tools():
    return SentimentAnalyzer()

analyzer = load_tools()

if st.sidebar.button("Analyser"):
    with st.spinner(f"Récupération des news pour {ticker}..."):
        # Récupération des données
        loader = FinancialDataLoader(ticker)
        news_data = loader.get_stock_news()
        
        if news_data:
            st.subheader(f"Dernières news pour {ticker}")
            
            # Préparation des données pour l'affichage
            results = []
            for item in news_data[:10]:
                ia_result = analyzer.analyze(item['title'])
                results.append({
                    "Date/Titre": item['title'],
                    "Sentiment API": item['api_sentiment'],
                    "Sentiment IA": ia_result['label'],
                    "Confiance IA": ia_result['score']
                })
            
            # Création d'un tableau Pandas pour l'affichage
            df = pd.DataFrame(results)
            
            # Affichage du tableau
            st.table(df)
            
            # Petit résumé visuel
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Nb News Analysées", len(df))
            with col2:
                # On compte combien de fois l'IA est positive
                pos_count = len(df[df['Sentiment IA'] == 'positive'])
                st.metric("News Positives (IA)", pos_count)
        else:
            st.error("Aucune donnée trouvée ou erreur API.")