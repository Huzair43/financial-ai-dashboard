import streamlit as st
import pandas as pd
from src.data_loader import FinancialDataLoader
from src.sentiment_analyzer import SentimentAnalyzer
from src.logger import PredictionLogger
import altair as alt
import sqlite3

DB_PATH = "data/predictions.db"

# -------------------------
# Fonctions utilitaires
# -------------------------
@st.cache_resource
def load_ai():
    analyzer = SentimentAnalyzer()
    logger = PredictionLogger()
    return analyzer, logger

@st.cache_data(ttl=60)
def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM predictions", conn)
    conn.close()
    return df

# -------------------------
# Initialisation
# -------------------------
analyzer, logger = load_ai()

st.set_page_config(page_title="AI Finance Dashboard", layout="wide", page_icon="📈")
st.title("📊 Financial AI Sentiment Dashboard")

# -------------------------
# Navigation onglets
# -------------------------
tab1, tab2 = st.tabs(["🔎 Analyse", "📊 Dashboard"])

# -------------------------
# Onglet Analyse
# -------------------------
with tab1:
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

    # Barre latérale
    with st.sidebar:
        st.header("🔎 Recherche")
        target_ticker = st.text_input("Ticker", value="TSLA").upper()
        nb_news = st.slider("Nombre d'articles", 3, 15, 5)
        st.divider()
        btn_run = st.button("Lancer l'Analyse", use_container_width=True)

    if btn_run:
        with st.spinner(f"Analyse de {target_ticker} en cours..."):
            loader = FinancialDataLoader(target_ticker)
            news_data = loader.get_stock_news(target_ticker)

            if news_data is None:
                st.error("🔑 Clé API manquante. Vérifiez votre fichier .env")
            elif not news_data:
                st.warning(f"Aucune donnée trouvée pour {target_ticker}.")
            else:
                results = []
                for item in news_data[:nb_news]:
                    ia_res = analyzer.analyze(item['title'])
                    # Log
                    logger.log(
                        ticker=target_ticker,
                        text=item['title'],
                        api_sentiment=item['api_sentiment'],
                        api_score=item['api_score'],
                        model_label=ia_res['label'],
                        model_score=ia_res['score'],
                        model_version=analyzer.version
                    )
                    results.append({**item, "ia_label": ia_res['label'], "ia_score": ia_res['score']})

                df = pd.DataFrame(results)

                # Métriques
                m1, m2, m3 = st.columns(3)
                m1.metric("Articles", len(df))
                pos_pct = (len(df[df['ia_label'] == 'positive']) / len(df)) * 100
                m2.metric("Sentiment IA", f"{pos_pct:.0f}% Positif")
                m3.metric("Confiance IA", f"{df['ia_score'].mean():.1%}")

                st.divider()

                # Affichage des News
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
        st.info("Saisissez un ticker pour commencer.")

# -------------------------
# Onglet Dashboard
# -------------------------
with tab2:
    df = load_data()
    if df.empty:
        st.warning("Aucune donnée disponible. Analyse d'abord des articles pour remplir la DB.")
    else:
        tickers = df['ticker'].unique().tolist()
        selected_ticker = st.selectbox("Sélectionnez un ticker", tickers)
        df_ticker = df[df['ticker'] == selected_ticker]
        df_ticker['timestamp'] = pd.to_datetime(df_ticker['timestamp'])
        df_sorted = df_ticker.sort_values('timestamp')
        df_sorted['rolling_score'] = df_sorted['model_score'].rolling(window=3, min_periods=1).mean()

        st.subheader(f"Histogramme des labels IA pour {selected_ticker}")
        hist = alt.Chart(df_ticker).mark_bar().encode(
            x='model_label:N',
            y='count()',
            color='model_label:N'
        )
        st.altair_chart(hist, use_container_width=True)

        st.subheader(f"Score moyen IA (rolling) pour {selected_ticker}")
        line = alt.Chart(df_sorted).mark_line(point=True).encode(
            x='timestamp:T',
            y='rolling_score:Q',
            tooltip=['text', 'model_label', 'model_score']
        )
        st.altair_chart(line, use_container_width=True)

        st.subheader(f"Nombre d'articles par date pour {selected_ticker}")
        count_df = df_ticker.groupby(df_ticker['timestamp'].dt.date).size().reset_index(name='count')
        bar = alt.Chart(count_df).mark_bar().encode(
            x='timestamp:T',
            y='count:Q'
        )
        st.altair_chart(bar, use_container_width=True)