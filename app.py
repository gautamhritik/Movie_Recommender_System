# import streamlit as st
# import pickle
# import pandas as pd
# import requests
#
# def fetch_poster(movie_id):
#     response = requests.get(
#         "https://api.themoviedb.org/3/movie/{}?api_key=d11cafa73479c2d82c4ddfce5b87027c&language=en-US".format(movie_id)
#     )
#     data = response.json()
#     return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
#
#
# def recommend(movie):
#     movie_index = movies[movies['title'] == movie].index[0]
#     distances = similarity[movie_index]
#     movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
#
#     recommended_movies = []
#     recommended_movie_posters = []
#     for i in movies_list:
#         movie_id = movies.iloc[i[0]].movie_id
#         #fetch the movie poster from API
#         recommended_movie_posters.append(fetch_poster(movie_id))
#         recommended_movies.append(movies.iloc[i[0]].title)
#     return recommended_movies,recommended_movie_posters
#
# movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
# movies = pd.DataFrame(movies_dict)
#
# similarity = pickle.load(open('similarity.pkl', 'rb'))
#
# st.title('Movie Recommender System')
#
# selected_movie_name = st.selectbox(
#     'Select Movie Recommender System',
#     movies['title'].values)
#
# if st.button('Recommend Movies'):
#     names,posters = recommend(selected_movie_name)
#
#     col1, col2, col3, col4, col5 = st.columns(5)  # replace deprecated beta_columns
#     with col1:
#         st.text(names[0])
#         st.image(posters[0])
#     with col2:
#         st.text(names[1])
#         st.image(posters[1])
#     with col3:
#         st.text(names[2])
#         st.image(posters[2])
#     with col4:
#         st.text(names[3])
#         st.image(posters[3])
#     with col5:
#         st.text(names[4])
#         st.image(posters[4])



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


# import streamlit as st
# import pickle
# import pandas as pd
# import requests
# import numpy as np
# import time
# import os
# import gdown
# from requests.adapters import HTTPAdapter
# from urllib3.util.retry import Retry

# # =========================
# # CONFIG
# # =========================
# API_KEY = os.getenv("TMDB_API_KEY", "your_tmdb_api_key_here")

# SIMILARITY_FILE_ID = "https://drive.google.com/file/d/1lPhdlfZZHIQffeublLn4ukB_XQP5gnIG/view?usp=drive_link"

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
# # DOWNLOAD FILE (IF NOT EXISTS)
# # =========================
# import requests

# def download_similarity():
#     if not os.path.exists("similarity.pkl"):
#         file_id = SIMILARITY_FILE_ID
#         url = f"https://drive.google.com/uc?export=download&id={file_id}"

#         with st.spinner("Downloading similarity data..."):
#             session = requests.Session()
#             response = session.get(url, stream=True)

#             # Handle large file confirmation
#             for key, value in response.cookies.items():
#                 if key.startswith("download_warning"):
#                     url = f"https://drive.google.com/uc?export=download&confirm={value}&id={file_id}"
#                     response = session.get(url, stream=True)
#                     break

#             with open("similarity.pkl", "wb") as f:
#                 for chunk in response.iter_content(32768):
#                     if chunk:
#                         f.write(chunk)


# import os
# st.write("File size:", os.path.getsize("similarity.pkl"))                        

# # =========================
# # FETCH POSTER
# # =========================
# def fetch_poster(movie_id):
#     try:
#         url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
#         response = session.get(url, timeout=5)

#         if response.status_code != 200:
#             return "https://via.placeholder.com/500x750?text=API+Error"

#         data = response.json()
#         poster_path = data.get('poster_path')

#         if poster_path:
#             return "https://image.tmdb.org/t/p/w500/" + poster_path
#         else:
#             return "https://via.placeholder.com/500x750?text=No+Poster"

#     except:
#         return "https://via.placeholder.com/500x750?text=Error"

# # =========================
# # LOAD DATA
# # =========================
# @st.cache_data
# def load_data():
#     download_similarity()

#     movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
#     similarity = pickle.load(open('similarity.pkl', 'rb'))

#     return pd.DataFrame(movies_dict), similarity

# movies, similarity = load_data()

# # =========================
# # RECOMMEND FUNCTION
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
#         time.sleep(0.2)

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
API_KEY = os.getenv("TMDB_API_KEY", "your_tmdb_api_key_here")

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
# def download_similarity():
#     if not os.path.exists("similarity.pkl"):
#         url = f"https://drive.google.com/uc?id={SIMILARITY_FILE_ID}"

#         with st.spinner("Downloading similarity data (first run)..."):
#             gdown.download(url, "similarity.pkl", quiet=False, fuzzy=True)

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
            return "https://via.placeholder.com/500x750?text=API+Error"

        data = response.json()
        poster_path = data.get('poster_path')

        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster"

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