import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def generate_time_series():
    np.random.seed(1)
    dates = pd.date_range(start='2020-01-01', periods=100)
    data = pd.DataFrame({
        'Date': dates,
        'Sales': np.random.randint(100, 200, size=100).cumsum()
    })
    return data

def show():
    st.header("Section 2: Trends and Changes")
    st.write("Exploration of time series or trend-based data.")

    data = generate_time_series()
    st.subheader("Sales Over Time")
    fig, ax = plt.subplots()
    ax.plot(data['Date'], data['Sales'], label='Sales')
    ax.set_xlabel('Date')
    ax.set_ylabel('Sales')
    ax.set_title('Sales Trend')
    ax.legend()
    st.pyplot(fig)

    st.subheader("Monthly Sales Bar Chart")
    data['Month'] = data['Date'].dt.month
    monthly_sales = data.groupby('Month')['Sales'].sum().reset_index()
    fig, ax = plt.subplots()
    sns.barplot(x='Month', y='Sales', data=monthly_sales, ax=ax)
    ax.set_title('Monthly Sales')
    st.pyplot(fig)
