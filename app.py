import streamlit as st
import pickle
import pandas as pd
import difflib

# ----------------------------------
# Load precomputed data
# ----------------------------------
movies_data = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

# ----------------------------------
# Recommendation Function
# ----------------------------------
def recommend(movie_name):
    index = movies_data[movies_data['title'] == movie_name].index[0]
    similarity_scores = list(enumerate(similarity[index]))

    sorted_movies = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )[1:6]

    return [movies_data.iloc[i[0]]['title'] for i in sorted_movies]

# ----------------------------------
# Streamlit UI
# ----------------------------------
st.set_page_config(
    page_title="Movie Recommendation System",
    layout="centered"
)

# ---- CSS for bold button ----
st.markdown(
    """
    <style>
    div.stButton > button {
        font-weight: bold;
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.markdown(
    "<h1 style='text-align:center;'>🎬 Movie Recommendation System</h1>",
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

# Bold input label
st.markdown(
    "<b>Enter your favorite movie 🎬</b>",
    unsafe_allow_html=True
)

# Text input
movie_input = st.text_input(
    "",
    placeholder="Type a movie name and press Recommend"
)

# Button
if st.button("Recommend"):
    if movie_input.strip() == "":
        st.warning("Please enter a movie name.")
    else:
        movie_titles = movies_data['title'].tolist()
        close_matches = difflib.get_close_matches(movie_input, movie_titles)

        if close_matches:
            selected_movie = close_matches[0]

            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader("Recommended Movies")

            for movie in recommend(selected_movie):
                st.write("👉", movie)
        else:
            st.error("Movie not found in database. Please try another title.")
