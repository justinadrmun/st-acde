import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

RATIO_ANNOTATIONS: dict = {
        0.66: '2x more \nmale than female \nrelations in the DAAO',
        0.75: '3x',
        0.80: '4x',
        0.90: '9x'
    }

def add_jitter_to_dataframe(df, columns, jitter_amounts, seed=1021):
    """Add random jitter to specified columns in a dataframe."""
    np.random.seed(seed)
    df_copy = df.copy()

    for col, jitter in zip(columns, jitter_amounts):
        df_copy[f"{col}_jittered"] = np.where(
            df_copy[col] != 1.0,
            df_copy[col] + np.random.normal(0, jitter/2, len(df)),
            df_copy[col]
        )
    return df_copy

def annotate_point(ax, x, y, label, color, position='right'):
    """Add an annotated point to the plot."""
    ax.scatter(x, y, color=color)
    
    text_props = {
        'textcoords': 'offset points',
        'fontsize': 8,
        'color': color,
        'alpha': 0.8,
        'bbox': dict(facecolor='white', edgecolor=color, boxstyle='round,pad=0.3', alpha=0.2)
    }
    
    if position == 'right':
        text_props.update({'xytext': (5, 0), 'ha': 'left'})
    else:
        text_props.update({'xytext': (-5, 0), 'ha': 'right'})
    
    ax.annotate(label, (x, y), **text_props)

def add_proportion_lines(ax, proportions, annot_pos=(12.5, 12.15)):
    """Add reference lines and annotations for proportions."""
    for prop, label in proportions.items():
        ax.axvline(x=prop, color='gray', linestyle='--', alpha=0.2)
        y_pos = annot_pos[1] if prop == 0.66 else annot_pos[0]
        ax.annotate(label, (prop, y_pos), fontsize=10, color='gray', ha='center', va='center')

def create_scatter_plot(df, x_col, y_col, annotations, proportions, xlabel, ylabel, x_limits, y_limits, seed, jitter=[0.05, 0.2]):
    """Generalized scatter plot creator with optional jitter and annotations."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    df = add_jitter_to_dataframe(df, [x_col, y_col], jitter, seed)
    x_data, y_data = f"{x_col}_jittered", f"{y_col}_jittered"

    for i, row in df.iterrows():
        color, position = annotations.get(i, ('tab:blue', 'right'))
        annotate_point(ax, row[x_data], row[y_data], row['Artist'], color, position)
    
    if "fe" in x_col:
        add_proportion_lines(ax, proportions, annot_pos=(52, 51.15))
    else:
        add_proportion_lines(ax, proportions)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xlim(*x_limits)
    ax.set_ylim(*y_limits)
    st.pyplot(fig)

def plot_male_relations(more_than_double_male_relations):
    """Create scatter plot of male relations proportion vs total relations."""
    annotations = {i: ('tab:orange' if i % 2 == 0 else 'tab:green', 'left' if i % 2 == 0 else 'right') 
                   for i in more_than_double_male_relations.index}
    create_scatter_plot(
        df=more_than_double_male_relations,
        x_col='"male"_proportion',
        y_col='All',
        annotations=annotations,
        proportions=RATIO_ANNOTATIONS,
        xlabel='Proportion of male relations',
        ylabel='Total relations',
        x_limits=(0.6, 1.05),
        y_limits=(4.5, 13),
        seed=1021,
    )

def plot_female_relations(more_than_double_female_relations):
    """Create scatter plot of female relations proportion vs total relations."""
    annotations = {}
    for i,_ in more_than_double_female_relations.iterrows():
        if i % 3 == 0:
            annotations[i] = ('tab:blue', 'right')
        elif i % 2 == 0:
            annotations[i] = ('tab:green', 'right')
        else:
            annotations[i] = ('tab:orange', 'left')
    
    create_scatter_plot(
        df=more_than_double_female_relations,
        x_col='"female"_proportion',
        y_col='All',
        annotations=annotations,
        proportions=RATIO_ANNOTATIONS,
        xlabel='Proportion of female relations',
        ylabel='Total relations',
        x_limits=(0.55, 1.05),
        y_limits=(0, 55),
        seed=1011,
        jitter=[0.125, 0.2]
    )