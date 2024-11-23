import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from utils import fetch_plot_data_for_archie_timeline

def setup_plot(data):
    """Create and configure the base plot."""
    fig, axes = plt.subplots(
        data.shape[1], 
        1, 
        figsize=(9, data.shape[1]*0.8), 
        sharex=True
    )
    return fig, axes

def normalize_data(data):
    """Normalize the data by subtracting 1 and setting negative values to 0."""
    normalized = data - 1
    normalized[normalized < 0] = 0
    return normalized

def add_gridlines(ax):
    """Add horizontal gridlines at y=1 and y=2."""
    for y_pos in [1, 2]:
        ax.axhline(y_pos, color='grey', linestyle='-', lw=0.5, alpha=0.2)

def add_annotations(ax):
    """Add text annotations for participation and win markers."""
    annotation_style = dict(
        ha='left', 
        va='center', 
        size=6,
        bbox=dict(
            boxstyle='round', 
            facecolor='white', 
            edgecolor='grey', 
            alpha=0.5
        )
    )
    
    ax.annotate('Participation', xy=(0.75, 1), **annotation_style)
    ax.annotate('Win', xy=(0.75, 2), **annotation_style)

def configure_axes(ax, col, color):
    """Configure the appearance of each subplot axis."""
    ax.set_title(col, x=0.9, y=0.6, size=7)
    ax.set_ylim(0, 3.5)
    ax.set_xlim(-1, 111)
    ax.axvspan(-1, 111, alpha=0.025, color=color)
    ax.set_yticks([])
    ax.tick_params(axis='x', labelsize=10.5)

def plot_timeline():
    """Create an artist timeline visualization."""
    artist_df = fetch_plot_data_for_archie_timeline()
    data = artist_df.T
    data = normalize_data(data)
    
    fig, axes = setup_plot(data)
    
    for idx, (col, ax) in enumerate(zip(data.columns, axes)):
        color = 'orange' if idx % 2 else 'green'
        
        if idx == 0:
            ax = ax.twiny()
            
        # Plot data series
        data[col].plot(ax=ax, rot=0)
        
        # Mark first win if exists
        series_data = pd.DataFrame(data[col])
        if len(series_data[series_data[col] == 2]):
            first_win = series_data[series_data[col] == 2].index[0]
            ax.axvline(first_win, color='r', linestyle='--', lw=1, alpha=0.7)
        
        add_gridlines(ax)
        add_annotations(ax)
        configure_axes(ax, col, color)
    
    st.pyplot(fig)