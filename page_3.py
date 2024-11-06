import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def generate_comparison_data():
    np.random.seed(2)
    data = pd.DataFrame({
        'Group': np.random.choice(['Control', 'Treatment'], size=100),
        'Score': np.random.normal(loc=50, scale=10, size=100)
    })
    return data

def show():
    st.header("Section 3: Comparisons")
    st.write("Comparison between different groups or categories.")

    data = generate_comparison_data()
    st.subheader("Grouped Bar Chart")
    group_means = data.groupby('Group')['Score'].mean().reset_index()
    fig, ax = plt.subplots()
    sns.barplot(x='Group', y='Score', data=group_means, ax=ax)
    ax.set_title('Average Score by Group')
    st.pyplot(fig)

    st.subheader("Box Plot")
    fig, ax = plt.subplots()
    sns.boxplot(x='Group', y='Score', data=data, ax=ax)
    ax.set_title('Score Distribution by Group')
    st.pyplot(fig)

    st.subheader("Violin Plot")
    fig, ax = plt.subplots()
    sns.violinplot(x='Group', y='Score', data=data, ax=ax)
    ax.set_title('Score Violation by Group')
    st.pyplot(fig)
