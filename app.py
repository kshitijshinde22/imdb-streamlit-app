import streamlit as st
import pandas as pd

# ------------------------------
# Load data
# ------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv('clean_imdb_movies.csv')
    df.replace('\\N', pd.NA, inplace=True)
    numeric_cols = ['startYear', 'runtimeMinutes', 'averageRating', 'numVotes']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df.dropna(subset=['startYear', 'averageRating', 'numVotes'], inplace=True)
    df = df[df['titleType'] == 'movie']
    df = df[df['numVotes'] >= 1000]
    df.reset_index(drop=True, inplace=True)
    return df

movies_df = load_data()

# ------------------------------
# Custom CSS
# ------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Poppins:wght@400;700&display=swap');

body {
    font-family: 'Poppins', sans-serif;
    background-color: #f5f5f5;
}

h1, h2, h3 {
    font-family: 'Montserrat', sans-serif;
}

.card {
    background: white;
    border-radius: 15px;
    padding: 15px;
    margin-bottom: 15px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

</style>
""", unsafe_allow_html=True)

# ------------------------------
# App Header
# ------------------------------
st.markdown("<h1 style='text-align: center; color: #4B4BFF;'>IMDb Movie Finder</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555;'>Search movies by title and get top-rated info instantly!</p>", unsafe_allow_html=True)
st.write("---")

# ------------------------------
# Search bar
# ------------------------------
search_query = st.text_input("Search a movie title:")

if search_query:
    results = movies_df[movies_df['primaryTitle'].str.contains(search_query, case=False, na=False)]
    
    if results.empty:
        st.warning(f"No movies found for '{search_query}'")
    else:
        for _, movie in results.iterrows():
            with st.container():
                st.markdown(f"""
                <div class="card">
                    <h3>{movie['primaryTitle']} ({int(movie['startYear'])})</h3>
                    <p><b>Genres:</b> {movie['genres']}</p>
                    <p><b>Rating:</b> {movie['averageRating']} ⭐ ({int(movie['numVotes'])} votes)</p>
                    <p><b>Runtime:</b> {movie['runtimeMinutes']} minutes</p>
                </div>
                """, unsafe_allow_html=True)
