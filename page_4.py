import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def generate_tab1():
        st.write("""
                    Is it possible to trace the distinction/relation between women in KMN who had a partner 
                    that was evidently impactful in terms of their networks and/or career and those who also 
                    had (or just had) a collaborator of some kind; a double act, mutually-enabling 
                    partnership? 
                 """
        )

def generate_tab2():
        st.write("""
                    Moving beyond the singular database – different identities as artists, e.g. Justin’s IMDB work etc.
                 """
        )

def generate_tab3():
        st.write("""
                    Marketplace analysis. Could we somehow showcase a few women from the exhibition who have the most ‘distinctive’ or ‘prestigious’ careers?
                 """
        )

page4_dict = {
    'Partnerships': generate_tab1,
    'Identity': generate_tab2,
    'Marketplace': generate_tab3
}


def show():
        st.header("Iconicity and Portfolio Careers")

        tabs = st.tabs(list(page4_dict.keys()))
        for i, tab in enumerate(tabs):
                with tab:
                        page4_dict[list(page4_dict.keys())[i]]()