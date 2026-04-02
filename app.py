# import streamlit as st
# import pickle
# import pandas as pd
# import requests
# import numpy as np
# import time
# import os
# from requests.adapters import HTTPAdapter
# from urllib3.util.retry import Retry

# # =========================
# # CONFIG
# # =========================
# API_KEY = os.getenv("TMDB_API_KEY", "d11cafa73479c2d82c4ddfce5b87027c")

# # =========================
# # SESSION WITH RETRY
# # =========================
# session = requests.Session()

# retries = Retry(
#     total=3,
#     backoff_factor=1,
#     status_forcelist=[500, 502, 503, 504]
# )

# session.mount("https://", HTTPAdapter(max_retries=retries))

# # =========================
# # FETCH POSTER (SAFE)
# # =========================
# def fetch_poster(movie_id):
#     try:
#         url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
#         response = session.get(url, timeout=5)

#         print("STATUS:", response.status_code)
#         print("RESPONSE:", response.text)

#         if response.status_code != 200:
#             return "https://via.placeholder.com/500x750?text=API+Error"

#         data = response.json()

#         poster_path = data.get('poster_path')

#         if poster_path:
#             return "https://image.tmdb.org/t/p/w500/" + poster_path
#         else:
#             return "https://via.placeholder.com/500x750?text=No+Poster"

#     except Exception as e:
#         print("ERROR:", e)
#         return "https://via.placeholder.com/500x750?text=Error"
# # =========================
# # LOAD DATA (CACHED)
# # =========================
# @st.cache_data
# def load_data():
#     movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
#     similarity = pickle.load(open('similarity.pkl', 'rb'))
#     return pd.DataFrame(movies_dict), similarity

# movies, similarity = load_data()

# # =========================
# # RECOMMEND FUNCTION (OPTIMIZED)
# # =========================
# def recommend(movie):
#     if movie not in movies['title'].values:
#         return [], []

#     movie_index = movies[movies['title'] == movie].index[0]
#     distances = similarity[movie_index]

#     movie_indices = np.argsort(distances)[::-1][1:6]

#     recommended_movies = []
#     recommended_posters = []

#     for i in movie_indices:
#         movie_id = movies.iloc[i].movie_id
#         recommended_movies.append(movies.iloc[i].title)
#         recommended_posters.append(fetch_poster(movie_id))
#         time.sleep(0.2)  # prevent API hammering

#     return recommended_movies, recommended_posters

# # =========================
# # UI
# # =========================
# st.title('🎬 Movie Recommender System')

# selected_movie_name = st.selectbox(
#     'Select a movie',
#     movies['title'].values
# )

# if st.button('Recommend'):
#     names, posters = recommend(selected_movie_name)

#     if not names:
#         st.error("Movie not found.")
#     else:
#         cols = st.columns(5)

#         for i in range(5):
#             with cols[i]:
#                 st.text(names[i])
#                 st.image(posters[i])



import streamlit as st
import pickle
import pandas as pd
import requests
import numpy as np
import time
import os
import gdown
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# =========================
# CONFIG
# =========================
API_KEY = st.secrets["TMDB_API_KEY"]

# ✅ ONLY FILE ID (NOT LINK)
SIMILARITY_FILE_ID = "1lPhdlfZZHIQffeublLn4ukB_XQP5gnIG"

# =========================
# SESSION WITH RETRY
# =========================
session = requests.Session()

retries = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[500, 502, 503, 504]
)

session.mount("https://", HTTPAdapter(max_retries=retries))

# =========================
# DOWNLOAD FILE
# =========================

def download_similarity():
    # ALWAYS delete corrupted file
    if os.path.exists("similarity.pkl"):
        if os.path.getsize("similarity.pkl") < 100000000:  # less than ~100MB = bad file
            os.remove("similarity.pkl")

    if not os.path.exists("similarity.pkl"):
        url = f"https://drive.google.com/uc?id={SIMILARITY_FILE_ID}"

        with st.spinner("Downloading similarity data (first run)..."):
            gdown.download(url, "similarity.pkl", quiet=False, fuzzy=True)

# =========================
# FETCH POSTER
# =========================
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
        response = session.get(url, timeout=5)

        if response.status_code != 200:
            return "https://via.placeholder.com/500x750?text=API+Fail"

        data = response.json()

        if not data.get("poster_path"):
            return "https://via.placeholder.com/500x750?text=No+Image"

        return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]

    except:
        return "https://via.placeholder.com/500x750?text=Error"

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    download_similarity()

    movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))

    return pd.DataFrame(movies_dict), similarity

movies, similarity = load_data()

# =========================
# RECOMMEND FUNCTION
# =========================
def recommend(movie):
    if movie not in movies['title'].values:
        return [], []

    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movie_indices = np.argsort(distances)[::-1][1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_indices:
        movie_id = movies.iloc[i].movie_id
        recommended_movies.append(movies.iloc[i].title)
        recommended_posters.append(fetch_poster(movie_id))
        time.sleep(0.2)

    return recommended_movies, recommended_posters

# =========================
# UI
# =========================
st.title('🎬 Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    if not names:
        st.error("Movie not found.")
    else:
        cols = st.columns(5)

        for i in range(5):
            with cols[i]:
                st.text(names[i])
                st.image(posters[i])