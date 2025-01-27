import streamlit as st
from custom_plot_funcs.protean_career_timeline import protean_career_timeline

#### George Gittoes' career over time ####
def generate_tab1():
    color_col = st.columns([1, 1, 1])
    with color_col[0]:
        st.write("Control colours of the plot using the colour pickers:")
        reset_colors = st.button("Reset colors")

    with color_col[1]:
        color_cols = st.columns([1, 1, 1], gap="small")
        with color_cols[0]:
            st.header("**AusStage**")
            austage_color = st.color_picker("Pick A Color", "#2ca02c", key="austage_color", help="Original hex color: #2ca02c")
        with color_cols[1]:
            st.header("**DAAO**")
            daao_color = st.color_picker("Pick A Color", "#1f77b4", key="daao_color", help="Original hex color: #1f77b4")
        with color_cols[2]:
            st.header("**IMDB**")
            imdb_color = st.color_picker("Pick A Color", "#ff7f0e", key="imdb_color", help="Original hex color: #ff7f0e")

    st.divider()

    if reset_colors:
        fig = protean_career_timeline()
    else:
        fig = protean_career_timeline(austage_color, daao_color, imdb_color)

    st.columns([0.8, 1.1, 1])[1].pyplot(fig)

def show():
    st.header("George Gittoes")
    generate_tab1()