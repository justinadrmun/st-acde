import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def generate_data():
    np.random.seed(0)
    data = pd.DataFrame({
        'Category': np.random.choice(['A', 'B', 'C', 'D'], size=100),
        'Value1': np.random.randn(100),
        'Value2': np.random.rand(100) * 100,
        'Value3': np.random.randint(0, 100, size=100)
    })
    return data

def show():
    st.header("Section 1: Overview")
    st.write("General summary of the dataset.")

    data = generate_data()
    st.subheader("Data Distribution")
    fig, ax = plt.subplots()
    sns.histplot(data['Value1'], kde=True, ax=ax)
    st.pyplot(fig)

    st.subheader("Basic Statistics")
    st.write(data.describe())
