import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def generate_summary_data():
    np.random.seed(4)
    data = pd.DataFrame({
        'Metric': ['Revenue', 'Profit', 'Growth', 'Retention'],
        'Value': [np.random.randint(1000, 5000),
                  np.random.randint(200, 1000),
                  np.random.uniform(5, 20),
                  np.random.uniform(70, 100)]
    })
    return data

def show():
    st.header("Section 5: Summary and Insights")
    st.write("Summary insights based on the visualizations from previous sections.")

    data = generate_summary_data()
    st.subheader("Summary Metrics")
    st.table(data)

    st.subheader("Final Correlation Plot")
    synthetic_data = pd.DataFrame({
        'Metric1': np.random.rand(50),
        'Metric2': np.random.rand(50),
        'Metric3': np.random.rand(50)
    })
    corr = synthetic_data.corr()
    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap='magma', ax=ax)
    ax.set_title('Final Correlation Matrix')
    st.pyplot(fig)
