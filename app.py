import pickle
import streamlit as st
import requests


st.set_page_config(
    page_title="Movie Recommender System",  # Title shown on the browser tab
    page_icon="🎬",  # You can use emojis or a URL to an icon
#     layout="wide",  # Optional: "centered" or "wide"
#     # initial_sidebar_state="expanded"  # Optional: "auto", "expanded", "collapsed"
)


# def fetch_poster(movie_id):
#     url = "https://api.themoviedb.org/3/movie/{}?api_key=7c0f6d327b3365bdbfc2b66d06cc254c&language=en-US".format(movie_id)
#     data = requests.get(url)
#     data = data.json()
#     poster_path = data['poster_path']
#     full_path = "https://image.tmdb.org/t/p/w500" + poster_path
#     return full_path
#
#
# def recommend(movie):
#     index = movies[movies['title'] == movie].index[0]
#     distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
#     recommended_movie_names = []
#     recommended_movie_posters = []
#     for i in distances[1:6]:
#         # fetch the movie poster
#         movie_id = movies.iloc[i[0]].movie_id
#         recommended_movie_posters.append(fetch_poster(movie_id))
#         recommended_movie_names.append(movies.iloc[i[0]].title)
#
#     return recommended_movie_names,recommended_movie_posters


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=7c0f6d327b3365bdbfc2b66d06cc254c&language=en-US"
    try:
        response = requests.get(url, timeout=5)  # Set timeout to 5 seconds
        response.raise_for_status()  # Raise HTTP errors (4xx, 5xx)
        data = response.json()
        poster_path = data.get('poster_path')
        full_path = "https://image.tmdb.org/t/p/w500" + poster_path
        return full_path

    except requests.exceptions.ConnectTimeout:
        st.error("Connection timed out. Please check your internet or try again later.")
        return "https://via.placeholder.com/500x750?text=Timeout"

    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
        return "https://via.placeholder.com/500x750?text=Error"


# Recommend movies
def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movie_names = []
        recommended_movie_posters = []
        for i in distances[1:6]:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movie_posters.append(fetch_poster(movie_id))
            recommended_movie_names.append(movies.iloc[i[0]].title)
        return recommended_movie_names, recommended_movie_posters
    except Exception as e:
        st.error(f"Error fetching recommendations: {e}")
        return [], []


st.markdown("<h1 style='text-align: center;'>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)


movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))


movie_list = movies['title'].values
selected_movie = st.selectbox(
    "🔎 Choose a movie:",
    movie_list
)


if st.button('Show Recommendation'):
    names, posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(posters[0])
        st.text(names[0])
    with col2:
        st.image(posters[1])
        st.text(names[1])
    with col3:
        st.image(posters[2])
        st.text(names[2])
    with col4:
        st.image(posters[3])
        st.text(names[3])
    with col5:
        st.image(posters[4])
        st.text(names[4])