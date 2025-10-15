import streamlit as st
import pandas as pd

# ------------------------------
# Load Data
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
# Custom CSS for dark theme & cool cards
# ------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Poppins:wght@400;700&display=swap');

body, .stApp {
    background-color: #121212;
    color: #E0E0E0;
    font-family: 'Poppins', sans-serif;
}

h1, h2, h3 {
    font-family: 'Montserrat', sans-serif;
    color: #FFCC00;
}

input, .stTextInput>div>div>input {
    background-color: #1E1E1E;
    color: #E0E0E0;
    border-radius: 10px;
    padding: 10px;
    border: 1px solid #333;
}

.card {
    background: linear-gradient(145deg, #1e1e1e, #272727);
    border-radius: 20px;
    padding: 25px;
    margin-bottom: 20px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.7);
    transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 35px rgba(0,0,0,0.8);
}

.top-movie {
    border: 2px solid #FFCC00;
    background: linear-gradient(145deg, #272727, #1e1e1e);
}

h4 {
    color: #FFD700;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------
# App Header
# ------------------------------
st.markdown("<h1 style='text-align: center;'>IMDb Movie Finder</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #B0B0B0;'>Search by year & genre or by movie title!</p>", unsafe_allow_html=True)
st.write("---")

# ------------------------------
# User Inputs
# ------------------------------
st.markdown("### Search by Year & Genre")
col1, col2 = st.columns(2)
with col1:
    year_input = st.text_input("Enter release year (e.g., 2023):")
with col2:
    genre_input = st.text_input("Enter genre (e.g., Action, Comedy):")

st.markdown("### Or Search by Movie Title")
title_input = st.text_input("Enter movie title:")

# ------------------------------
# Search Functions
# ------------------------------
def find_top_movies(year, genre, top_n=3):
    try:
        year = int(year)
    except:
        return None, "Please enter a valid year."

    subset = movies_df[(movies_df['startYear'] == year) & 
                       (movies_df['genres'].str.contains(genre, case=False, na=False))]
    if subset.empty:
        return None, f"No {genre} movies found in {year} with at least 1000 votes."

    subset = subset.sort_values(by=['averageRating', 'numVotes'], ascending=False).reset_index()
    return subset.head(top_n), None

def find_movie_by_title(title):
    subset = movies_df[movies_df['primaryTitle'].str.contains(title, case=False, na=False)]
    if subset.empty:
        return None, "Movie not found."

    movie = subset.iloc[0]
    # Ranking in that year by numVotes
    year_movies = movies_df[movies_df['startYear'] == movie['startYear']].sort_values(by='numVotes', ascending=False).reset_index()
    rank = year_movies[year_movies['primaryTitle'] == movie['primaryTitle']].index[0] + 1

    return movie, rank

# ------------------------------
# Show Results
# ------------------------------
# 1️⃣ Year & Genre search
if year_input and genre_input:
    top_movies, error = find_top_movies(year_input, genre_input)
    if error:
        st.warning(error)
    else:
        # Show top 1 prominently
        main_movie = top_movies.iloc[0]
        st.markdown(f"""
        <div class="card top-movie">
            <h2>{main_movie['primaryTitle']} ({int(main_movie['startYear'])})</h2>
            <p><b>Genres:</b> {main_movie['genres']}</p>
            <p><b>Rating:</b> {main_movie['averageRating']} ⭐ ({int(main_movie['numVotes'])} votes)</p>
            <p><b>Runtime:</b> {main_movie['runtimeMinutes']} minutes</p>
        </div>
        """, unsafe_allow_html=True)

        # Show next top 2 movies
        if len(top_movies) > 1:
            st.markdown("<h3 style='color:#FFCC00;'>Other Top Movies:</h3>", unsafe_allow_html=True)
            for i in range(1, len(top_movies)):
                movie = top_movies.iloc[i]
                st.markdown(f"""
                <div class="card">
                    <h4>{movie['primaryTitle']} ({int(movie['startYear'])})</h4>
                    <p><b>Genres:</b> {movie['genres']}</p>
                    <p><b>Rating:</b> {movie['averageRating']} ⭐ ({int(movie['numVotes'])} votes)</p>
                </div>
                """, unsafe_allow_html=True)

# 2️⃣ Search by Title
if title_input:
    movie, rank_or_error = find_movie_by_title(title_input)
    if movie is None:
        st.warning(rank_or_error)
    else:
        st.markdown("<h3 style='color:#FFCC00;'>Movie Details & Year Ranking</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="card top-movie">
            <h2>{movie['primaryTitle']} ({int(movie['startYear'])})</h2>
            <p><b>Genres:</b> {movie['genres']}</p>
            <p><b>Rating:</b> {movie['averageRating']} ⭐ ({int(movie['numVotes'])} votes)</p>
            <p><b>Runtime:</b> {movie['runtimeMinutes']} minutes</p>
            <p><b>Ranking in {int(movie['startYear'])} by votes:</b> #{rank_or_error}</p>
        </div>
        """, unsafe_allow_html=True)
