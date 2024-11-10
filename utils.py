import pandas as pd
import streamlit as st
import numpy as np

def fetch_kmn_data():
    return pd.read_csv("data/kmn_with_related_data.csv")

def center_figure(plot_func, *args, **kwargs):
    _, col2, _ = st.columns([1, 5, 1])
    with col2:
        plot_func(*args, **kwargs)