import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def generate_tab1():
        st.write("""
                    What is the relationship between the material that appears publicly in the ‘end point’ of 
                    the exhibition and the material on which the curatorial process draws? In other words, to 
                    create KMN exhibition? 
                 """
        )

def generate_tab2():
        st.write("""
                    Who legitimates artists – function of critics, commentators (the change to online commentary)? 
                 """
        )

def generate_tab3():
        st.write("""
                    Is there material in AustLit about people in KMN (i.e. writers who are also visual artists) 
                 """
        )

def generate_tab4():
        st.write("""
                    Key words that constellate around women’s art criticism as they appear in the KMN critical book and 
                    cognate art/literary criticism  ")
                """
        )

def generate_tab5():
        st.write("""
                    In what sense does ‘feminism’ represent white women? 
                """)
        
def generate_tab6():
        st.write("""
                    Link between Anne Marsh entries (in the dataset) and material that appears in other collections
                """
        )

page3_dict = {
    'Curatorial Process': generate_tab1,
    'Legitimation': generate_tab2,
    'AustLit': generate_tab3,
    'Key Words': generate_tab4,
    'Feminism': generate_tab5,
    'Anne Marsh entries': generate_tab6
}

def show():
        st.header("Art criticism and its impact on the KMN reception and legacy")

        tabs = st.tabs(list(page3_dict.keys()))
        for i, tab in enumerate(tabs):
                with tab:
                        page3_dict[list(page3_dict.keys())[i]]()