import pandas as pd
import matplotlib.pyplot as plt

def population_pyramid(major_vs_regional, remove_yticks=False):
    """
    Plot population pyramid of major vs regional galleries for KMN artists
    """  
    index = major_vs_regional["artist"].unique()

    title0 = 'Major galleries'
    title1 = 'Regional galleries'
    
    # population pyramid of major vs regional galleries for KMN artists
    fig, axes = plt.subplots(figsize=(10,5),ncols=2, sharey=True)
    fig.tight_layout()
    axes[0].barh(major_vs_regional["artist"].unique(), 
                 major_vs_regional["is_large_gallery"], 
                 align='center', color='tab:orange', zorder=10)
    axes[0].set_title('Major galleries', pad=15, color='tab:orange')

    axes[1].barh(major_vs_regional["artist"].unique(), 
                 major_vs_regional["is_regional_gallery"], 
                 align='center', color='tab:blue', zorder=10)
    axes[1].set_title('Regional galleries', pad=15, color='tab:blue')

    # increase x-axis limit with increments of 5
    axes[0].set_xlim(0, major_vs_regional["is_large_gallery"].max() + 5)
    axes[1].set_xlim(0, major_vs_regional["is_large_gallery"].max() + 5)

    # If you have positive numbers and want to invert the x-axis of the left plot
    axes[0].invert_xaxis() 

    # To show data from highest to lowest
    plt.gca().invert_yaxis()

    axes[0].set(yticks=major_vs_regional["artist"].unique(), 
                yticklabels=major_vs_regional["artist"].unique())
    axes[0].yaxis.tick_left()

    plt.subplots_adjust(wspace=0, top=0.85, bottom=0.1, left=0.18, right=0.95)

    # remove x and y axis tick labels and tick marks
    if remove_yticks:
        axes[0].set_yticks([])
        axes[1].set_yticks([])

    return fig