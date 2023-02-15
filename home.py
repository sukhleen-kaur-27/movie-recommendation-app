import streamlit as st

def recommend_movies(movie_name, similarity_df, all_movies_ratings):
  similar_movies = similarity_df[str(movie_name)]
  similar_movies_df = pd.DataFrame(similar_movies)
  similar_movies_df.rename(columns = {similar_movies_df.columns[0]: 'correlation'}, inplace = True)
  corr_num_ratings = similar_movies_df.join(all_movies_ratings['num of ratings'])
  return corr_num_ratings[corr_num_ratings['num of ratings'] > 100].sort_values('correlation',ascending = False).head(20)

def app(similarity_df,all_movies_ratings):
  st.header('Movie Recommendation System')
  st.write('This web app allows a user to get movie recommendations based on popularity, genre and rating, along with some visuals a peek into the actual data.')
  st.text("")
  movie_name = st.text_input("Enter a movie name to get similar recommendations :")
  hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

  # Inject CSS with Markdown
  st.markdown(hide_table_row_index, unsafe_allow_html=True)
  if st.button("Search"):
    st.table(recommend_movies(movie_name, similarity_df, all_movies_ratings))