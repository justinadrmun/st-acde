import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def generate_tab1():
        st.markdown("""
                    - A visualization of women in the KMN group who have changed their names at some 
                    point, either before or after the exhibition or over the course of their careers  
                    - Names as they appear differently in different collections/databases?
                 """
        )

def generate_tab2():
        st.write("Names of KMN artists who have different last names in different collections")

def generate_tab3():
        st.markdown("""
                    - Married names, gender neutral names, Indigenous names, (e.g. the Knagwareye controversy), fabricated or pseudonyms 
                    """
        )

page2_dict = {
    'Name changes': generate_tab1,
    'Different last names': generate_tab2,
    'Other': generate_tab3
}

def show():
        st.header("Name and changes of name + the significance of name in determining career")
        tabs = st.tabs(list(page2_dict.keys()))
        for i, tab in enumerate(tabs):
                with tab:
                        page2_dict[list(page2_dict.keys())[i]]()