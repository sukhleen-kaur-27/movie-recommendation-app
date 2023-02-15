	

import streamlit as st


def app(top_20_popular):
	st.header("Movie Recommedation System")
	st.subheader("Recommedation based on Popularity : ")
	hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

	# Inject CSS with Markdown
	st.markdown(hide_table_row_index, unsafe_allow_html=True)
	st.table(top_20_popular.drop(columns=["id", "genres"]))