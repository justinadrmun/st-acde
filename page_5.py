import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def generate_tab1():
        st.write("""
                    Have all of the KMN women had their work exhibited in a ‘major’ Australian gallery? In 
                    other words, in putting the KMN list together, was a curatorial decision made (either 
                    explicitly or indirectly) about the connection between significance of an artist and where 
                    their work was shown? 
                 """
        )

def generate_tab2():
        st.write("""
                    TLCMap to show whether KMN involved a deceptive geographical spread; distinguishes 
                    Indigenous artists from urban artists 
                 """
        )

def generate_tab3():
        st.write("""
                    International mobilities – might we show some artists on a map who have also moved 
                    and worked/exhibited beyond Australia
                 """
        )

def generate_tab4():
        st.write("Could we visualize those in KMN who had work shown in major galleries vs regional (minor galleries)")

def generate_tab5():
        st.write("""
                    Can we map the locality/relations of collective arts practices where they are explicitly 
                    identified in KMN – away from individuation of authorship. 
                """)
        
def generate_tab6():
        st.write("Social media representations")

def generate_tab7():
       st.write("Everyone in the KMN dataset and location of birth")

page5_dict = {
    "Major Galleries": generate_tab1,
    "TLCMap": generate_tab2,
    "International Mobilities": generate_tab3,
    "Major vs Regional": generate_tab4,
    "Collective Arts Practices": generate_tab5,
    "Social Media": generate_tab6,
    "Location of Birth": generate_tab7
}

def show():
        st.header("The Boundaries of Experience")

        tabs = st.tabs(list(page5_dict.keys()))
        for i, tab in enumerate(tabs):
                with tab:
                        page5_dict[list(page5_dict.keys())[i]]()