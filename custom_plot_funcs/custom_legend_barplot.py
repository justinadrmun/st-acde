from utils import fetch_daao_kmn_alt_names
import matplotlib.pyplot as plt
import streamlit as st

def add_new_lines(s):
    """Insert newlines into a string for better readability."""
    words = s.split(' ')
    new_s = ''
    for i, word in enumerate(words):
        if i % 3 == 0 and i != 0:
            new_s += '\n'
        new_s += word + ' '
    return new_s

def fetch_and_filter_alt_names():
    """Fetch alternative names and filter those with counts greater than one."""
    alt_names = fetch_daao_kmn_alt_names()
    return alt_names.display_name.value_counts()[alt_names.display_name.value_counts() > 1].sort_values()

def create_color_map(categories):
    """Create a color map for the given categories."""
    return {category: color for category, color in zip(categories, ['tab:blue', 'tab:green', 'tab:orange', 'tab:red'])}

def plot_alternative_names():
    """Generate and display the alternative names bar plot."""
    alt_names_many = fetch_and_filter_alt_names()
    alt_names_cats = alt_names_cats_unique = alt_names_cats = fetch_daao_kmn_alt_names().category.unique()
    alt_names_cats_cmap = create_color_map(alt_names_cats)
    
    fig, ax = plt.subplots(figsize=(14, 10))
    alt_names_many.plot(kind='barh', color='white', ax=ax, linewidth=3, width=0.89)
    
    for i, count in enumerate(alt_names_many):
        this_alt = fetch_daao_kmn_alt_names()[fetch_daao_kmn_alt_names().display_name == alt_names_many.index[i]].reset_index()
        for j, row in this_alt.iterrows():
            ax.add_patch(plt.Rectangle((j, i-0.3), width=0.99, height=0.8, fill=True, alpha=0.8,
                                       color=alt_names_cats_cmap[row.category]))
            label = add_new_lines(str(row.alternative_names))
            ax.text(j+0.05, i, label, color='black', va='center', fontsize=8.5)
    
    customize_plot(ax, alt_names_cats, alt_names_cats_cmap)
    st.pyplot(fig)

def customize_plot(ax, categories, color_map):
    """Apply customizations to the plot."""
    plt.xlim(0, 5.1)
    plt.yticks(fontsize=10)
    plt.grid(color='white', linestyle='-', linewidth=1, axis='x')
    plt.title(' ', fontsize=24)
    plt.ylabel('')
    plt.xlabel('No. of alternative names')
    
    add_legend(ax, categories, color_map)

def add_legend(ax, categories, color_map):
    """Add a horizontal legend for categories on the top of the plot."""
    legend_y = 14
    ax.text(1.8, legend_y, 'Legend:', color='black', fontsize=10, va='center', fontweight='bold')
    positions = [2.2, 3.2, 3.5, 4.2]
    for pos, category in zip(positions, categories):
        ax.text(pos, legend_y, category, color=color_map[category], fontsize=10, va='center',
                bbox=dict(facecolor='white', edgecolor=color_map[category], boxstyle='round,pad=0.3'))