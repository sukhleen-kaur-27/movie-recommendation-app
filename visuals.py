import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.set_option('deprecation.showPyplotGlobalUse', False)
@st.cache(suppress_st_warning=True)
def app(genre_table, top_20_popular):
	st.subheader("Top 20 Popular Movies")
	plt.figure(figsize = (12, 6))
	sns.barplot(x='popularity', y= 'title', data = top_20_popular)
	plt.title("Top 20 popular movies")
	st.pyplot()





	st.subheader("Popular Genres")
	plt.figure(figsize=(12,6))
	plt.title("Popular Genres")
	sns.barplot(data = genre_table.sort_values('popularity', ascending = False), y = 'genres',
	            x = 'popularity')
	st.pyplot()




	st.subheader("Most Voted Genres")
	plt.figure(figsize = (12, 6))
	plt.title("Most Voted Genres")
	sns.barplot(data = genre_table.sort_values('vote_count', ascending = False), 
	            y = 'genres', x = 'vote_count')
	st.pyplot()
