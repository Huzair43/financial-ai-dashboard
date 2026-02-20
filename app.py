import streamlit as st
import pandas as pd
from src.data_loader import FinancialDataLoader
from src.sentiment_analyzer import SentimentAnalyzer

# Configuration
st.set_page_config(page_title="AI Finance Dashboard", layout="wide", page_icon="📈")

# Style CSS pour les cartes
st.markdown("""
    <style>
    .news-card {
        background-color: #f9f9f9; padding: 18px; border-radius: 8px;
        border-left: 5px solid #007bff; margin-bottom: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .sentiment-label { font-weight: bold; font-size: 0.85em; }
    </style>
    """, unsafe_allow_html=True)

# Initialisation de l'IA (une seule fois)
@st.cache_resource
def load_ai():
    return SentimentAnalyzer()

analyzer = load_ai()

# Barre latérale
with st.sidebar:
    st.header("🔎 Recherche")
    target_ticker = st.text_input("Ticker", value="TSLA").upper()
    nb_news = st.slider("Nombre d'articles", 3, 15, 5)
    st.divider()
    btn_run = st.button("Lancer l'Analyse", use_container_width=True)

st.title("📊 Financial AI Sentiment Dashboard")

if btn_run:
    with st.spinner(f"Analyse de {target_ticker} en cours..."):
        # 1. Instanciation
        loader = FinancialDataLoader(target_ticker)
        
        # 2. Récupération (On passe target_ticker pour le cache !)
        news_data = loader.get_stock_news(target_ticker)
        
        if news_data is None:
            st.error("🔑 Clé API manquante. Vérifiez votre fichier .env")
        elif not news_data:
            st.warning(f"Aucune donnée trouvée pour {target_ticker}.")
        else:
            # 3. Analyse IA
            results = []
            for item in news_data[:nb_news]:
                ia_res = analyzer.analyze(item['title'])
                results.append({**item, "ia_label": ia_res['label'], "ia_score": ia_res['score']})
            
            df = pd.DataFrame(results)

            # 4. Métriques
            m1, m2, m3 = st.columns(3)
            m1.metric("Articles", len(df))
            pos_pct = (len(df[df['ia_label'] == 'positive']) / len(df)) * 100
            m2.metric("Sentiment IA", f"{pos_pct:.0f}% Positif")
            m3.metric("Confiance IA", f"{df['ia_score'].mean():.1%}")

            st.divider()

            # 5. Affichage des News
            for _, row in df.iterrows():
                color = "#28a745" if row['ia_label'] == "positive" else "#dc3545" if row['ia_label'] == "negative" else "#6c757d"
                
                st.markdown(f"""
                <div class="news-card">
                    <h4 style="margin:0;"><a href="{row['url']}" target="_blank" style="color:#1f2937; text-decoration:none;">{row['title']}</a></h4>
                    <p style="color:#4b5563; font-size:0.9em; margin: 8px 0;">{row['summary'][:250]}...</p>
                    <span class="sentiment-label" style="color:{color};">🤖 IA: {row['ia_label'].upper()} ({row['ia_score']:.1%})</span>
                    <span style="margin-left:20px; color:#9ca3af; font-size:0.8em;">🔌 API: {row['api_sentiment']}</span>
                </div>
                """, unsafe_allow_html=True)
else:
    st.info("Saisissez un ticker (ex: NVDA, BTC, AAPL) pour commencer.")