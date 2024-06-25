# import streamlit as st
# import pickle
# import pandas as pd
# import requests

# def fetch_poster(movie_id):
#     # response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=e8e8d4120aaa4bf0ee410b3bfd49e3eb&language=en-US'.format(movie_id))
#     # data = response.json()
#     # poster_path = data['poster_path']
#     # full_paht = "https://image.tmdb.org/t/p/w500/" + poster_path
#     # return full_paht
#     # url = "https://api.themoviedb.org/3/movie/{}?api_key=e8e8d4120aaa4bf0ee410b3bfd49e3eb&language=en-US".format(movie_id)
#     # response = requests.get(url)
#     # data = response.json()
#     # poster_path = data['poster_path']
#     # full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
#     # return full_path

# def recommend(movie):
#     movie_index = movies[movies['title'] == movie].index[0]
#     distances = similarity[movie_index]
#     movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

#     recommended_movies = []
#     recommended_movies_posters = []
#     for i in movies_list:
#         movie_id = movies.iloc[i[0]].movie_id
#         recommended_movies.append(movies.iloc[i[0]].title)
#         recommended_movies_posters.append(fetch_poster(movie_id))
#     return recommended_movies, recommended_movies_posters

# # Load movie data and similarity matrix
# movies_dict = pickle.load(open('movies_dict1.pkl', 'rb'))
# movies = pd.DataFrame(movies_dict)

# similarity = pickle.load(open('similarity.pkl', 'rb'))

# st.title('Movie Recommender System')

# selected_movie_name = st.selectbox('Select a movie', movies['title'].values)

# if st.button('Recommend'):
#     recommended_movies, recommended_movies_posters = recommend(selected_movie_name)
    
#     columns = st.columns(5)
#     for col, movie, poster in zip(columns, recommended_movies, recommended_movies_posters):
#         with col:
#             st.text(movie)
#             st.image(poster)
# import streamlit as st
# import pickle 
# import pandas as pd
# import requests

# def fetch_poster(movie_id):
#     try:#https://api.themoviedb.org/3/movie/{movie_id}?api_key=8c07c5775c9ad9d64d0e40f7a0d21fcc&language=en-US

#         response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8c07c5775c9ad9d64d0e40f7a0d21fcc&language=en-US')
#         response.raise_for_status()
#         data = response.json()
#         poster_path = data['poster_path']
#         full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
#         return full_path
#     except Exception as e:
#         st.error(f"Error fetching poster: {str(e)}")
#         return None

# def recommend(movie):
#     try:
#         movie_index = movies[movies['title'] == movie].index[0]
#         distances = similarity[movie_index]
#         movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]

#         recommend_movies = []
#         recommend_movies_poster = []
#         for i in movies_list:
#             movie_id = movies.iloc[i[0]].movie_id
#             recommend_movies.append(movies.iloc[i[0]].title)
#             poster = fetch_poster(movie_id)
#             recommend_movies_poster.append(poster if poster else "No poster available")
#         return recommend_movies, recommend_movies_poster
#     except Exception as e:
#         st.error(f"Error in recommendation: {str(e)}")
#         return [], []

# st.title('Movie Recommender System')

# try:
#     movies_dict = pickle.load(open('movies_dict1.pkl', 'rb'))
#     movies = pd.DataFrame(movies_dict)
#     similarity = pickle.load(open('similarity.pkl', 'rb'))
    
#     st.write("Data loaded successfully")
#     st.write(f"Number of movies: {len(movies)}")
    
#     selected_movie_name = st.selectbox('Select a movie', movies['title'].values)

#     if st.button('Recommend'):
#         st.write("Recommendation button clicked")
#         recommend_movies, recommend_movies_poster = recommend(selected_movie_name)
        
#         if recommend_movies and recommend_movies_poster:
#             col1, col2, col3, col4, col5 = st.columns(5)
#             for i, (movie, poster) in enumerate(zip(recommend_movies, recommend_movies_poster)):
#                 with [col1, col2, col3, col4, col5][i]:
#                     st.text(movie)
#                     st.image(poster)
#         else:
#             st.write("No recommendations available")

# except Exception as e:
#     st.error(f"An error occurred: {str(e)}")
import streamlit as st
import pickle 
import pandas as pd
import requests

def fetch_poster(movie_id):
    try:
        url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'
        response = requests.get(url)
        response.raise_for_status()  # This will raise an exception for HTTP errors
        data = response.json()
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
    except KeyError:
        st.error(f"Poster path not found for movie ID: {movie_id}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
    return None

def recommend(movie):
    try:
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]

        recommend_movies = []
        recommend_movies_poster = []
        for i in movies_list:
            movie_id = movies.iloc[i[0]].movie_id
            st.write(f"Fetching poster for movie ID: {movie_id}")  # Debug line
            poster = fetch_poster(movie_id)
            if poster:
                recommend_movies.append(movies.iloc[i[0]].title)
                recommend_movies_poster.append(poster)
            else:
                st.warning(f"Could not fetch poster for {movies.iloc[i[0]].title}")
        return recommend_movies, recommend_movies_poster
    except Exception as e:
        st.error(f"Error in recommendation: {str(e)}")
        return [], []

st.title('Movie Recommender System')

try:
    movies_dict = pickle.load(open('movies_dict1.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    
    st.write("Data loaded successfully")
    st.write(f"Number of movies: {len(movies)}")
    
    selected_movie_name = st.selectbox('Select a movie', movies['title'].values)

    if st.button('Recommend'):
        st.write("Recommendation button clicked")
        recommend_movies, recommend_movies_poster = recommend(selected_movie_name)
        
        if recommend_movies and recommend_movies_poster:
            col1, col2, col3, col4, col5 = st.columns(5)
            columns = [col1, col2, col3, col4, col5]
            for i, (movie, poster) in enumerate(zip(recommend_movies, recommend_movies_poster)):
                with columns[i]:
                    st.text(movie)
                    st.image(poster)
        else:
            st.write("No recommendations available")

except FileNotFoundError as e:
    st.error(f"File not found: {e}")
except Exception as e:
    st.error(f"An error occurred: {str(e)}")

# Add this at the end to see if the script runs to completion
st.write("Script completed execution")