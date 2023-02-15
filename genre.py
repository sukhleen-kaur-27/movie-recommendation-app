import streamlit as st


def genre_recommender(fav_genre, genre_based_df):
  	recommended_df = genre_based_df[genre_based_df['genres'] == fav_genre]
  	return(recommended_df.head(25))

def app(genre_based_df, genre_table):
	st.header("Popular Movies based in Genre")
	st.text("")
	st.subheader("Top 3 Popular genres :")
	beta_col1, beta_col2, beta_col3=st.beta_columns(3)
	with beta_col1:
		st.write(genre_table["genres"][0])
	with beta_col2:
		st.write(genre_table["genres"][1])
	with beta_col3:
		st.write(genre_table["genres"][2])


	st.text("")

	genre_name=st.selectbox('Select your favourite genre : ', tuple(genre_based_df["genres"]))
	
	genre_t = genre_recommender(genre_name, genre_based_df).drop(columns = ["id","genres"])
	title_series = genre_t.pop("title")
	genre_t.insert(loc= 0, column = "Title", value = title_series)
	hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

	# Inject CSS with Markdown
	st.markdown(hide_table_row_index, unsafe_allow_html=True)
	if st.button("Show Results"):
		st.table(genre_t)


	