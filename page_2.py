import streamlit as st

from utils import fetch_daao_kmn_alt_names, inspect_data
from custom_plot_funcs.custom_legend_barplot import plot_alternative_names
from custom_plot_funcs.custom_legend_barplot_v2 import plot_alternative_names_v2

def generate_tab1():
        st.caption("""
                    - A visualization of women in the KMN group who have changed their names at some 
                    point, either before or after the exhibition or over the course of their careers  
                    - Names as they appear differently in different collections/databases?
                    - Names of KMN artists who have different last names in different collections
                 """
        )
        st.divider()
        alt_names_frame = fetch_daao_kmn_alt_names()
        st.write("**KMN artists in the DAAO with alternative names**")

        cols = st.columns([1, 1, 2])
        with cols[0]:
                st.metric("Number of KMN artists with alternative names", 
                        alt_names_frame.display_name.nunique())
        with cols[1]:
                st.metric("Number of alternative name occurrences", 
                        alt_names_frame.shape[0])
                st.metric("Average number of alternative names per artist",
                        round(alt_names_frame.shape[0]/alt_names_frame.display_name.nunique(), 2))
                     
        with cols[2]:
                st.write("**Alternative name categories**")
                st.bar_chart(alt_names_frame.category.value_counts(), horizontal=True)
        st.divider()
        st.write("**KMN artists who have more than one alternative name in the DAAO**")
        if st.button("Inspect data :mag_right:"):
                inspect_data(alt_names_frame)
        cols = st.columns([3, 1, 1])
        with cols[0]:
                plot_alternative_names()

def generate_tab2():
        st.write("**KMN artists in the DAAO with alternative names**")
        alt_names_frame2 = fetch_daao_kmn_alt_names(v2=True)

        cols = st.columns([1, 1, 2])
        with cols[0]:
                st.metric("Number of KMN artists with alternative names", 
                        alt_names_frame2["Know My Name"].nunique())
        with cols[1]:
                st.metric("Number of alternative name occurrences", 
                        alt_names_frame2.shape[0])
                st.metric("Average number of alternative names per artist",
                        round(alt_names_frame2.shape[0]/alt_names_frame2["Know My Name"].nunique(), 2))
                     
        with cols[2]:
                st.write("**Alternative name categories**")
                st.bar_chart(alt_names_frame2["category (SoN)"].value_counts(), horizontal=True)
        st.divider()
        st.write("**KMN artists who have more than one alternative name in the DAAO**")
        if st.button("Inspect (updated) data :mag_right:"):
                inspect_data(alt_names_frame2)
        cols = st.columns([3, 1, 1])
        with cols[0]:
                plot_alternative_names_v2()

def generate_tab3():
        st.caption("""
                    - Married names, gender neutral names, Indigenous names, (e.g. the Knagwareye controversy), fabricated or pseudonyms 
                    """
        )

page2_dict = {
    'Name changes': generate_tab1,
    'Name changes (Data from Nat)': generate_tab2,
    'Other': generate_tab3
}

def show():
        st.header("Name and changes of name + the significance of name in determining career")
        tabs = st.tabs(list(page2_dict.keys()))
        for i, tab in enumerate(tabs):
                with tab:
                        page2_dict[list(page2_dict.keys())[i]]()