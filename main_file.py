from ast import literal_eval
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import streamlit as st
import home, popularity, genre, rating, visuals


st.set_page_config(page_title='Movie Recommedation System',
                   page_icon='blue',
                   layout='centered',
                   initial_sidebar_state='auto')



warnings.filterwarnings("ignore")

# Read the dataset and print first five records.
url = "https://drive.google.com/uc?id=1rPR-P45M2UWsbXc8vpyCzWcQAYUfgVJX"
movies_df = pd.read_csv(url)

mov_subset_df = movies_df[['genres', 'id', 'popularity', 'title', 'vote_average', 'vote_count']]

mov_subset_df = mov_subset_df.drop_duplicates(subset = ['id'])

mov_subset_df.dropna(inplace = True)

# Convert the type of 'id' column to 'int' type.
mov_subset_df['id'] = mov_subset_df['id'].astype('int')

# Convert the type of 'popularity' column to 'float' type.
mov_subset_df['popularity'] = mov_subset_df['popularity'].astype('float')

mov_subset_df['genres'] = mov_subset_df['genres'].apply(lambda x: [i['name'] for i in literal_eval(x)])

genres_subset_df = mov_subset_df.explode('genres', ignore_index = True)


top_20_popular = mov_subset_df.sort_values(by = 'popularity', ascending = False).head(20)
new_series = top_20_popular.pop("title")
top_20_popular.insert(loc = 0, column = "title", value = new_series)


parameters_df = genres_subset_df[['genres', 'popularity', 'vote_average', 'vote_count']]


genre_table = pd.pivot_table(parameters_df, index =['genres']).reset_index()



top_20_va = mov_subset_df.sort_values(by = 'vote_average', ascending = False).head(20)


C = mov_subset_df['vote_average'].mean()



m = mov_subset_df['vote_count'].quantile(0.9)


qualified_movies_df = mov_subset_df.copy().loc[mov_subset_df['vote_count'] >= m]

genre_based_df = qualified_movies_df.explode('genres', ignore_index = True)

def weighted_rating(df):
    v = df['vote_count']
    R = df['vote_average']
    
    # Calculation based on the Weighted Rating formula
    W = ((R * v) + (C * m)) / (v + m)
    return W



qualified_movies_df['weighted_rating'] = qualified_movies_df.apply(weighted_rating, axis= 1)
qualified_movies_df.head()

qualified_movies_df.sort_values(by= 'weighted_rating', ascending = False, inplace = True)
qualified_movies_df.head(25)






nav_list = ["Home", "Popularity", "Genre", "Rating", "Visuals"]
# Add radio buttons in the sidebar for navigation and call the respective pages based on 'user_choice'.
st.sidebar.header("Movie Recommedation System")
st.sidebar.title('Navigation')
user_choice=st.sidebar.radio('Go To', nav_list)



df = pd.read_csv('https://drive.google.com/uc?id=1zLq1138MYTTEJgHERmHG-FhuB8vfxfLY')

movies_df = df[['id', 'imdb_id', 'title']]
movies_df.dropna(inplace = True)

movies_df['id'] = movies_df['id'].astype('float')

links_df = pd.read_csv('https://drive.google.com/uc?id=1Hn83CnGeHG6evq274ztIm6VcOrImBOAF')
m_links_df = pd.merge(movies_df, links_df, left_on ='id', right_on ='tmdbId')
m_df = m_links_df[['movieId', 'title']]
ratings_df = pd.read_csv('https://drive.google.com/uc?id=17xgnHVj8in4SxBGh7j9daAbtYa2zz8fw')
ratings_df = ratings_df.drop('timestamp', axis=1)
final_movies_df = pd.merge(m_df, ratings_df, on = 'movieId')
all_movies_ratings = pd.DataFrame(final_movies_df.groupby('title')['rating'].mean())
all_movies_ratings['num of ratings'] = pd.DataFrame(final_movies_df.groupby('title')['rating'].count())
user_ratings = final_movies_df.pivot_table(index ='userId', columns ='title', values ='rating')
similarity_df = user_ratings.corr()




if user_choice=='Home':
  home.app(similarity_df,all_movies_ratings)
elif user_choice=="Popularity":
  popularity.app(top_20_popular)
elif user_choice=="Genre":
	genre.app(genre_based_df, genre_table)
elif user_choice=="Rating":
	rating.app(qualified_movies_df)
else :
	visuals.app(genre_table, top_20_popular)
