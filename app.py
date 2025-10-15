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
# Custom CSS for Dark Theme
# ------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Poppins:wght@400;700&display=swap');

body {
    font-family: 'Poppins', sans-serif;
    background-color: #121212;
    color: #E0E0E0;
}

h1, h2, h3 {
    font-family: 'Montserrat', sans-serif;
    color: #FFCC00;
}

input, .stTextInput>div>div>input {
    background-color: #1E1E1E;
    color: #E0E0E0;
    border-radius: 8px;
    padding: 8px;
    border: none;
}

.card {
    background: #1E1E1E;
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.7);
    color: #E0E0E0;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------
# App Header
# ------------------------------
st.markdown("<h1 style='text-align: center;'>IMDb Movie Finder</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #B0B0B0;'>Type release year & genre to find the top-rated movie!</p>", unsafe_allow_html=True)
st.write("---")

# ------------------------------
# User Inputs
# ------------------------------
col1, col2 = st.columns(2)
with col1:
    year_input = st.text_input("Enter release year (e.g., 2023):")
with col2:
    genre_input = st.text_input("Enter genre (e.g., Action, Comedy):")

# ------------------------------
# Search Function
# ------------------------------
def find_best_movie(year, genre):
    try:
        year = int(year)
    except:
        return None, "Please enter a valid year."

    subset = movies_df[(movies_df['startYear'] == year) & 
                       (movies_df['genres'].str.contains(genre, case=False, na=False))]

    if subset.empty:
        return None, f"No {genre} movies found in {year} with at least 1000 votes."

    best = subset.sort_values(by=['averageRating', 'numVotes'], ascending=False).iloc[0]
    return best, None

# ------------------------------
# Show Results
# ------------------------------
if year_input and genre_input:
    movie, error = find_best_movie(year_input, genre_input)
    if error:
        st.warning(error)
    else:
        st.markdown(f"""
        <div class="card">
            <h2>{movie['primaryTitle']} ({int(movie['startYear'])})</h2>
            <p><b>Genres:</b> {movie['genres']}</p>
            <p><b>Rating:</b> {movie['averageRating']} ⭐ ({int(movie['numVotes'])} votes)</p>
            <p><b>Runtime:</b> {movie['runtimeMinutes']} minutes</p>
        </div>
        """, unsafe_allow_html=True)
