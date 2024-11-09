import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def generate_tab1():
        st.write("""
                 Some kind of visualisation showing the ‘Top 10’ artists in the collection by way of how ‘visible’ 
                 they are in existing cultural databases. i.e. who from the KMN dataset appears the most in DAAO and Prints & Printmaking?
                 """
        )

def generate_tab2():
        st.write("""
                Some kind of visualisation where we have, say, 5 artists from the KMN collection, with a 
                little panel of 5 items of metadata about them (a line could then link out to a photograph 
                of one of their exhibition artworks)
                 """
        )

def generate_tab3():
        st.markdown("""
                 - KMN meets Archibald – data viz overview.
                 - Show women in the Archibald who also feature in KMN
                 """
        )

def generate_tab4():
        st.write("""
                 Data imagery – who is included/ relationship to DAAO, gender differences, geographic spread, date range for birth of subjects?
                """)
        
def generate_tab5():
        st.markdown("""
                 - Compare with data from Australia exhibition at Royal Academy in 2013 
                 - Rex Butler – decrying the lack of artistic judgment that data-driven/metric-based merit shows have on the discipline of art history 
                 - What happens when you datafy (or reverse engineer as data) an exhibition that happened in situ?
                    """
        )

page1_dict = {
    'Top 10': generate_tab1,
    '5 Artists': generate_tab2,
    'Archibald': generate_tab3,
    'DAAO': generate_tab4,
    'Other': generate_tab5
}

def show():
        st.header("Data comparisons")

        tabs = st.tabs(list(page1_dict.keys()))
        for i, tab in enumerate(tabs):
                with tab:
                        page1_dict[list(page1_dict.keys())[i]]()