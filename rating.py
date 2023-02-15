import streamlit as st

@st.cache_data()
def app(qualified_movies_df):
	st.header("Movies based on Rating using Weighted Rating")
	qualified_movies_df.sort_values(by= 'weighted_rating', ascending = False, inplace = True)
	title_column = qualified_movies_df.pop("title")
	qualified_movies_df.insert(loc = 0, column = "Title", value = title_column)

	hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

	# Inject CSS with Markdown
	st.markdown(hide_table_row_index, unsafe_allow_html=True)
	st.table(qualified_movies_df.drop(columns=["id", "genres"]))
