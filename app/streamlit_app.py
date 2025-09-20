
import os
import pandas as pd
import streamlit as st
import altair as alt

# ================================
# Streamlit Page Setup
# ================================
st.set_page_config(page_title="CORD-19 Data Explorer", layout="wide")

# ================================
# Load Data Function (Cached)
# ================================
@st.cache_data
def load_data():
    try:
        base_path = os.path.dirname(os.path.dirname(__file__))  # go up from /app
        data_path = os.path.join(base_path, "data", "metadata.csv")
        df = pd.read_csv(data_path, low_memory=False)

        # Clean & prepare
        df["year"] = pd.to_datetime(df["publish_time"], errors="coerce").dt.year
        df["abstract_word_count"] = df["abstract"].fillna("").apply(lambda x: len(x.split()))
        return df
    except FileNotFoundError:
        st.error("❌ Could not find metadata.csv in the /data folder.")
        return pd.DataFrame()

# ================================
# Load Data
# ================================
df = load_data()
if df.empty:
    st.stop()

# ================================
# UI Layout
# ================================
st.title("📊 CORD-19 Data Explorer")
st.markdown(
    """
Explore the CORD-19 dataset interactively: filter by year, view publication trends,
see top journals, and preview sample data.
"""
)

# ================================
# Filters
# ================================
min_year, max_year = int(df["year"].min()), int(df["year"].max())
year_range = st.slider("📅 Select Year Range", min_year, max_year, (min_year, max_year))

filtered_df = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]

# ================================
# Charts Section
# ================================
col1, col2 = st.columns(2)

# ---- Chart 1: Publications by Year ----
with col1:
    st.subheader("📈 Publications by Year")
    yearly_counts = filtered_df["year"].value_counts().sort_index().reset_index()
    yearly_counts.columns = ["year", "publication_count"]

    if not yearly_counts.empty:
        yearly_chart = alt.Chart(yearly_counts).mark_bar().encode(
            x=alt.X("year:O", title="Year"),
            y=alt.Y("publication_count:Q", title="Number of Publications"),
            tooltip=["year", "publication_count"]
        ).properties(height=400)
        st.altair_chart(yearly_chart, use_container_width=True)
    else:
        st.info("No data available for selected year range.")

# ---- Chart 2: Top Journals ----
with col2:
    st.subheader("🏢 Top 10 Journals")
    top_journals = (
        filtered_df["journal"]
        .dropna()
        .value_counts()
        .head(10)
        .reset_index()
    )
    top_journals.columns = ["journal", "publication_count"]

    if not top_journals.empty:
        journal_chart = alt.Chart(top_journals).mark_bar().encode(
            x=alt.X("publication_count:Q", title="Number of Papers"),
            y=alt.Y("journal:N", sort="-x", title="Journal"),
            tooltip=["journal", "publication_count"]
        ).properties(height=400)
        st.altair_chart(journal_chart, use_container_width=True)
    else:
        st.info("No journal data available for selected range.")

# ================================
# Search & Table
# ================================
st.subheader("🔎 Search Papers")
search_query = st.text_input("Search by title or author (case-insensitive):")

filtered_search_df = filtered_df
if search_query:
    filtered_search_df = filtered_df[
        filtered_df["title"].str.contains(search_query, case=False, na=False)
        | filtered_df["authors"].str.contains(search_query, case=False, na=False)
    ]

st.dataframe(filtered_search_df[["title", "publish_time", "year", "journal", "abstract_word_count"]].head(20))

# ================================
# Optional Stop Button
# ================================
if st.button("🛑 Stop Streamlit Server"):
    st.write("Shutting down...")
    import signal, os
    os.kill(os.getpid(), signal.SIGTERM)
