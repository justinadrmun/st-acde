import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns

from utils import fetch_george_gittoes_timeline_data

mcolors.TABLEAU_COLORS
mcolors.XKCD_COLORS
mcolors.CSS4_COLORS
#Base colors are in RGB so they need to be converted to HEX
BASE_COLORS_hex = {name:mcolors.rgb2hex(color) for name,color in mcolors.BASE_COLORS.items()}

all_named_colors = {}
all_named_colors.update(mcolors.TABLEAU_COLORS)
all_named_colors.update(BASE_COLORS_hex)
all_named_colors.update(mcolors.CSS4_COLORS)
all_named_colors.update(mcolors.XKCD_COLORS)

def protean_career_timeline(
    austage_color = 'tab:green',
    daao_color = 'tab:blue',
    imdb_color = 'tab:orange'
):
    if austage_color in all_named_colors:
        austage_color = all_named_colors[austage_color]
    if daao_color in all_named_colors:
        daao_color = all_named_colors[daao_color]
    if imdb_color in all_named_colors:
        imdb_color = all_named_colors[imdb_color]

    george_df = fetch_george_gittoes_timeline_data()
    g1 = george_df.copy()

    ausstage = george_df[george_df.Dataset == 'AusStage'].reset_index(drop=True)
    daao = george_df[george_df.Dataset == 'DAAO'].reset_index(drop=True)
    imdb = george_df[george_df.Dataset == 'IMDB'].reset_index(drop=True)

    g1 = g1[g1.Type != 'Residence']
    g1_awards = g1[(g1.Type == 'Recognition') | (g1.Type == 'Winner') | (g1.Type == 'Nominee')]
    g1 = g1[g1.Type != 'Winner']
    g1 = g1[g1.Type != 'Nominee']
    g1 = g1[g1.Type != 'Recognition']

    fig, ax = plt.subplots(figsize=(10,18))
    sns.scatterplot(data=g1.sort_values(['Dataset'], ascending=[True]),
    x='Dataset', y='Start', hue='Dataset', ax=ax, s=550, alpha=0.7, linewidth=7,
    palette=[austage_color,daao_color,imdb_color], legend=False)

    plt.scatter(data=g1[(g1.Country != 'Australia') & (~g1.Country.isnull())].sort_values(['Dataset'], ascending=[True]),
                x='Dataset',y='Start', marker='x', color='black', s=200, zorder=10)

    # change x-axis labels to be different colors
    for label in ax.get_xticklabels():
        dataset_label = label.get_text()
        if dataset_label == 'AusStage': label.set_color(austage_color)
        elif dataset_label == 'DAAO': label.set_color(daao_color)
        elif dataset_label == 'IMDB': label.set_color(imdb_color)

    sns.scatterplot(data=g1_awards[g1_awards.Type != 'Recognition'].sort_values(['Dataset'], ascending=[True]),
    x=3.75, y='Start', hue='Dataset', ax=ax, s=550, alpha=0.7, palette=[imdb_color], legend=True,linewidth=7)

    sns.scatterplot(data=g1_awards[g1_awards.Type == 'Recognition'].sort_values(['Dataset'], ascending=[True]),
    x=3.75, y='Start', hue='Dataset', ax=ax, s=550, alpha=0.7, palette=[daao_color], legend=True, linewidth=7)

    plt.legend(loc='lower left', fontsize=14, ncol=2, facecolor='white')
    # for i in range(6): plt.gca().get_legend().legendHandles[i]._sizes = [200]

    # make y-axis labels larger
    plt.yticks(fontsize=14); plt.xticks(fontsize=16)
    plt.ylabel(''); plt.xlabel('')

    # add y-axis grid
    plt.grid(axis='y', alpha=0.3)

    # add a title
    # plt.title("George Gittoes' career over time" , fontsize=16)
    plt.title("")

    # add higlighted rectangles centered at 0
    plt.axvspan(-0.25, 0.25, facecolor=austage_color, alpha=0.1)
    plt.axvspan(0.75, 1.25, facecolor=daao_color, alpha=0.1)
    plt.axvspan(1.75, 2.25, facecolor=imdb_color, alpha=0.1)


    # add vertical line
    # add a horizontal line  between the start and end of each person's career
    for idx,p in enumerate(daao[daao['Type'] == 'Residence'].sort_values('Start')['Event'].unique()):
        start = daao[(daao['Event']==p)]['Start'].min()
        end = daao[(daao['Event']==p)]['End'].max()
        if (start==end) | (start+1==end): 
            
            sns.scatterplot(data=daao[daao['Event']==p].sort_values(['Start'], ascending=[True]),
            x=-2.2, y='Start',hue='Event', ax=ax, s=550, alpha=0.15, palette=[daao_color], legend=False)

            plt.scatter(data=daao[(daao['Event']==p) & (daao.Country != 'Australia') & (~daao.Country.isnull())].sort_values(['Start'], ascending=[True]),
                x=-2.2,y=2009, marker='x', color='black', s=200, zorder=10)
            
        else:
            if idx % 2 == 0: plt.plot([-2,-2], [start+0.4, end-0.4], linewidth=24, zorder=0, color = daao_color, alpha=0.4)
            else: plt.plot([-2.2,-2.2], [start+0.4, end-0.4], linewidth=24, zorder=0, color = daao_color, alpha=0.15)


    # add annottation above the vertical line
    plt.annotate('Residence', (-2.35, g1['Start'].min()-1.5), fontsize=15, alpha=1, color='black')


    # add annottation above the vertical line
    plt.annotate('Recognition', (3.3, g1['Start'].min()-1.5), fontsize=15, alpha=1, color='black')


    # add text labels for each Residence event
    for idx,p in enumerate(daao[daao['Type'] == 'Residence'].sort_values('Start')['Event'].unique()):
        start = daao[(daao['Event']==p)]['Start'].min()
        end = daao[(daao['Event']==p)]['End'].max()
        if (start==end) | (start+1==end): 
            ax.annotate(p, (-2.3, start), fontsize=10, alpha=1, color=daao_color)
        else:
            if idx % 2 == 0: ax.annotate(p, (-2.3, (start+end)/2), fontsize=10, alpha=1, color=daao_color)
            else: ax.annotate(p, (-2.3, (start+end)/2), fontsize=10, alpha=1, color=daao_color)

    daao = daao[daao.Type != 'Residence']

    for idx,x in enumerate(ausstage['Type']):
        y = ausstage[ausstage.Type.str.contains(x)]['Start'][idx]
        ax.annotate(x, (-.65, y), fontsize=10, alpha=1, color=austage_color)

    for idx,x in enumerate(daao['Type'].unique()):
        y = george_df[(george_df.Dataset == 'DAAO') & (george_df.Type.str.contains(x))]['Start'].unique()
        for y in george_df[(george_df.Dataset == 'DAAO') & (george_df.Type.str.contains(x))]['Start'].unique():
            z = george_df[(george_df.Dataset == 'DAAO') & (george_df.Type.str.contains(x)) & (george_df.Start == y)]['Start'].iloc[0]
            if (x == 'Recognition'): ax.annotate(x, (3.95, z), fontsize=10, alpha=1, color=daao_color)
            else:
                if idx % 2 == 0: ax.annotate(x, (0.5, z), fontsize=10, alpha=1, color=daao_color)
                else: ax.annotate(x, (1.2, z), fontsize=10, alpha=1, color=daao_color)

    for idx,x in enumerate(imdb['Type'].unique()):
        y = george_df[(george_df.Dataset == 'IMDB') & (george_df.Type.str.contains(x))]['Start'].unique()
        for y in george_df[(george_df.Dataset == 'IMDB') & (george_df.Type.str.contains(x))]['Start'].unique():
            z = george_df[(george_df.Dataset == 'IMDB') & (george_df.Type.str.contains(x)) & (george_df.Start == y)]['Start'].iloc[0]
            if (x == 'Nominee'): ax.annotate(x, (3, z), fontsize=10, alpha=1, color=imdb_color)
            elif (x == 'Winner'): ax.annotate(x, (4, z), fontsize=10, alpha=1, color=imdb_color)
            else:
                ax.annotate(x, (2.25, z), fontsize=10, alpha=1, color=imdb_color)

    # change the order of the y-axis
    plt.gca().invert_yaxis()

    # add more space between the x-axis ticks
    plt.xticks(np.arange(0, 10, 1))

    # move legend to specific location
    # plt.legend(loc='upper right', fontsize=12, ncol=1, facecolor='white', bbox_to_anchor=(0.965, 0.97))
    # for i in range(2): plt.gca().get_legend().legendHandles[i]._sizes = [200]

    # remove the legend
    plt.legend().remove()

    # add vertical lines on 0,1,2
    plt.axvline(x=-.85, color='black', alpha=0.4, linestyle='-', linewidth=1)
    plt.axvline(x=2.95, color='black', alpha=0.4, linestyle='-', linewidth=1)
    # plt.axvline(x=0, color='lightgrey', alpha=0.4, linestyle='-', linewidth=1)
    # plt.axvline(x=1, color='lightgrey', alpha=0.4, linestyle='-', linewidth=1)
    # plt.axvline(x=2, color='lightgrey', alpha=0.4, linestyle='-', linewidth=1)

    # add horizontal lines
    plt.axhline(y=1949, color='black', alpha=0.3, linestyle='-', linewidth=1, xmin=0.52, xmax=0.61)
    plt.axhline(y=1971, color='black', alpha=0.3, linestyle='-', linewidth=1, xmin=0.385, xmax=0.48)
    plt.axhline(y=2006, color='black', alpha=0.3, linestyle='-', linewidth=1, xmin=0.52, xmax=0.61)


    # # add annotation top right of plot to denote the vertical lines
    # plt.annotate('| = annual break', xy=(2006.5, -.5), fontsize=12, alpha=0.5)

    #remove y-axis title
    plt.ylabel('')

    # increase y-axis limits to make room for the title
    plt.xlim(-2.75, 4.75)

    # # save figure with 300 dpi
    # plt.savefig('georgegittoes_timeline.png', dpi=330, bbox_inches='tight')

    return fig