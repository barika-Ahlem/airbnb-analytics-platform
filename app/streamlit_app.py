import streamlit as st
import duckdb
import pandas as pd
import os

# ── Configuration ──────────────────────────────────────────────────────────────
DB_PATH = os.path.join(os.path.dirname(__file__), "../data/airbnb.duckdb")

st.set_page_config(
    page_title="Airbnb Analytics Platform",
    page_icon="🏠",
    layout="wide"
)

@st.cache_resource
def get_connection():
    return duckdb.connect(DB_PATH, read_only=True)

con = get_connection()

# ── Header ─────────────────────────────────────────────────────────────────────
st.title("🏠 Airbnb Analytics Platform")
st.markdown("Tableau de bord analytique basé sur les données Airbnb")

# ── KPIs ───────────────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

nb_listings  = con.execute("SELECT COUNT(*) FROM gold.dim_listings").fetchone()[0]
nb_hosts     = con.execute("SELECT COUNT(*) FROM gold.dim_hosts").fetchone()[0]
nb_reviews   = con.execute("SELECT COUNT(*) FROM gold.fact_reviews").fetchone()[0]
nb_superhost = con.execute("SELECT COUNT(*) FROM gold.dim_hosts WHERE is_superhost = TRUE").fetchone()[0]

col1.metric("🏘️ Logements",     f"{nb_listings:,}")
col2.metric("👤 Hôtes",         f"{nb_hosts:,}")
col3.metric("💬 Avis",          f"{nb_reviews:,}")
col4.metric("⭐ Superhosts",    f"{nb_superhost:,}")

st.divider()

# ── Onglets ────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📋 Logements", "👤 Hôtes", "💬 Avis", "🌕 Pleine Lune"])

# ── TAB 1 : Logements ──────────────────────────────────────────────────────────
with tab1:
    st.subheader("Analyse des logements")

    # Filtre type de chambre
    room_types = con.execute("SELECT DISTINCT room_type FROM gold.dim_listings ORDER BY 1").df()["room_type"].tolist()
    selected_room = st.multiselect("Type de logement", room_types, default=room_types)

    df_listings = con.execute(f"""
        SELECT room_type, COUNT(*) AS nb, ROUND(AVG(price), 2) AS avg_price
        FROM gold.dim_listings
        WHERE room_type IN ({','.join(['?' for _ in selected_room])})
        GROUP BY room_type
        ORDER BY nb DESC
    """, selected_room).df()

    col_a, col_b = st.columns(2)
    with col_a:
        st.bar_chart(df_listings.set_index("room_type")["nb"], color="#FF5A5F")
        st.caption("Nombre de logements par type")
    with col_b:
        st.bar_chart(df_listings.set_index("room_type")["avg_price"], color="#00A699")
        st.caption("Prix moyen par type (€)")

    st.subheader("Top 10 logements les plus chers")
    df_top = con.execute("""
        SELECT listing_name, room_type, price, minimum_nights
        FROM gold.dim_listings
        ORDER BY price DESC LIMIT 10
    """).df()
    st.dataframe(df_top, use_container_width=True)

# ── TAB 2 : Hôtes ──────────────────────────────────────────────────────────────
with tab2:
    st.subheader("Analyse des hôtes")

    df_superhost = con.execute("""
        SELECT
            CASE WHEN is_superhost THEN 'Superhost ⭐' ELSE 'Hôte standard' END AS type_hote,
            COUNT(*) AS nb
        FROM gold.dim_hosts
        GROUP BY is_superhost
    """).df()

    col_a, col_b = st.columns(2)
    with col_a:
        st.bar_chart(df_superhost.set_index("type_hote"), color="#FF5A5F")
        st.caption("Répartition Superhost vs Standard")
    with col_b:
        df_host_listings = con.execute("""
            SELECT h.host_name, COUNT(*) AS nb_listings, ROUND(AVG(l.price),2) AS avg_price
            FROM gold.dim_hosts h
            JOIN gold.dim_listings l ON h.host_id = l.host_id
            GROUP BY h.host_name
            ORDER BY nb_listings DESC
            LIMIT 10
        """).df()
        st.dataframe(df_host_listings, use_container_width=True)
        st.caption("Top 10 hôtes par nombre de logements")

# ── TAB 3 : Avis ───────────────────────────────────────────────────────────────
with tab3:
    st.subheader("Analyse des avis clients")

    df_sentiment = con.execute("""
        SELECT sentiment, COUNT(*) AS nb
        FROM gold.fact_reviews
        WHERE sentiment IS NOT NULL
        GROUP BY sentiment
        ORDER BY nb DESC
    """).df()

    col_a, col_b = st.columns(2)
    with col_a:
        st.bar_chart(df_sentiment.set_index("sentiment"), color="#FC642D")
        st.caption("Distribution des sentiments")
    with col_b:
        df_reviews_time = con.execute("""
            SELECT DATE_TRUNC('month', review_date) AS month, COUNT(*) AS nb_reviews
            FROM gold.fact_reviews
            GROUP BY 1
            ORDER BY 1
        """).df()
        st.line_chart(df_reviews_time.set_index("month"), color="#00A699")
        st.caption("Évolution mensuelle des avis")

    # Filtre reviewer
    st.subheader("Filtrer par reviewer")
    reviewers = con.execute("""
        SELECT DISTINCT reviewer_name FROM gold.fact_reviews
        ORDER BY reviewer_name LIMIT 50
    """).df()["reviewer_name"].tolist()
    selected_reviewer = st.selectbox("Choisir un reviewer", reviewers)

    df_reviewer = con.execute("""
        SELECT review_date, review_text, sentiment
        FROM gold.fact_reviews
        WHERE reviewer_name = ?
        ORDER BY review_date DESC
    """, [selected_reviewer]).df()
    st.dataframe(df_reviewer, use_container_width=True)

# ── TAB 4 : Pleine Lune ────────────────────────────────────────────────────────
with tab4:
    st.subheader("Impact des nuits de pleine lune sur les avis")

    df_moon = con.execute("""
        SELECT is_full_moon, sentiment, COUNT(*) AS nb
        FROM gold.full_moon_reviews
        WHERE sentiment IS NOT NULL
        GROUP BY is_full_moon, sentiment
        ORDER BY is_full_moon, nb DESC
    """).df()

    df_pivot = df_moon.pivot(index="sentiment", columns="is_full_moon", values="nb").fillna(0)
    st.bar_chart(df_pivot, color=["#FF5A5F", "#00A699"])
    st.caption("Sentiments selon pleine lune ou non")

    st.subheader("Données détaillées")
    df_moon_detail = con.execute("""
        SELECT review_date, reviewer_name, sentiment, is_full_moon,
               LEFT(review_text, 200) AS apercu_avis
        FROM gold.full_moon_reviews
        ORDER BY review_date DESC
        LIMIT 100
    """).df()
    st.dataframe(df_moon_detail, use_container_width=True)

st.divider()
st.caption("Airbnb Analytics Platform — MBAESG 2026")