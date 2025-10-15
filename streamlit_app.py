import streamlit as st
import pandas as pd

# App title and layout
st.set_page_config(page_title="IMDb Movie Finder", layout="centered")

st.title("🎬 IMDb Movie Finder")
st.write("Search for the top-rated movies by year and genre!")

# Load dataset
data = pd.read_csv("clean_imdb_movies.csv")

# Sidebar filters
year = st.sidebar.selectbox("Select Year", sorted(data['startYear'].dropna().unique().astype(int)), index=0)
genre = st.sidebar.selectbox("Select Genre", sorted(data['genres'].dropna().unique()), index=0)

# Filter data
filtered = data[(data['startYear'] == year) & (data['genres'].str.contains(genre, case=False, na=False))]

if not filtered.empty:
    best_movie = filtered.loc[filtered['averageRating'].idxmax()]
    st.subheader("🎥 Best Rated Movie")
    st.write(f"**Title:** {best_movie['primaryTitle']}")
    st.write(f"**Year:** {int(best_movie['startYear'])}")
    st.write(f"**Genre:** {best_movie['genres']}")
    st.write(f"**IMDb Rating:** ⭐ {best_movie['averageRating']}")
else:
    st.warning("No movies found for the selected year and genre.")
