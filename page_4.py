import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def generate_relationship_data():
    np.random.seed(3)
    data = pd.DataFrame({
        'Height': np.random.normal(170, 10, 100),
        'Weight': np.random.normal(65, 15, 100),
        'Age': np.random.randint(18, 60, size=100)
    })
    return data

def show():
    st.header("Section 4: Relationships")
    st.write("Investigation of relationships between variables.")

    data = generate_relationship_data()
    st.subheader("Scatter Plot")
    fig, ax = plt.subplots()
    sns.scatterplot(x='Height', y='Weight', data=data, ax=ax)
    ax.set_title('Height vs Weight')
    st.pyplot(fig)

    st.subheader("Pair Plot")
    fig = sns.pairplot(data)
    st.pyplot(fig)

    st.subheader("Correlation Heatmap")
    corr = data.corr()
    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap='viridis', ax=ax)
    ax.set_title('Correlation Matrix')
    st.pyplot(fig)
