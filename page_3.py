import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from utils import fetch_daao_austlist_works

def generate_tab1():
        st.caption("""
                    Is there material in AustLit about people in KMN (i.e. writers who are also visual artists) 
                 """
        )
        frame = fetch_daao_austlist_works()
        # find out who has data for every section, if all_sections_count is 4, then the person has data for all sections
        frame['all_sections_count'] = frame[['agentWorksBy_count', 
                                             'agentWorksAbout_count', 
                                             'agentWorksWorks_count', 
                                             'AgentText_Awards_count']]\
                                        .sum(axis=1)
        frame_populated = frame[frame.all_sections_count == 4].copy()

        st.write(f"**Artists that exist in KMN, DAAO and Austlit (n={len(frame)}):**")
        cols = st.columns(5)
        for idx, artist in enumerate(frame.found):
                with cols[idx % 5]:
                        st.metric(value="", 
                                  label=f"{artist}*" if artist in frame_populated.found.values else artist)
        st.write("")
        st.caption("*Artists that have data for all sections - agentWorksBy, agentWorksAbout, agentWorksWorks, AgentText_Awards")
        st.divider()

        fig, ax = plt.subplots()
        # create a new dataframe for the counts
        counts = pd.DataFrame({
        'agentWorksBy': [frame.agentWorksBy_count.sum(), frame.shape[0] - frame.agentWorksBy_count.sum()],
        'agentWorksAbout': [frame.agentWorksAbout_count.sum(), frame.shape[0] - frame.agentWorksAbout_count.sum()],
        'agentWorksWorks': [frame.agentWorksWorks_count.sum(), frame.shape[0] - frame.agentWorksWorks_count.sum()],
        'AgentText_Awards': [frame.AgentText_Awards_count.sum(), frame.shape[0] - frame.AgentText_Awards_count.sum()]
        }, index=['True', 'False'])

        # plot the clustered bar chart
        counts = counts.T.iloc[::-1]
        counts.plot(kind='barh', stacked=False, ax=ax)

        # add bar labels for each bar, trie and false counts
        for i in ax.patches:
            ax.text(i.get_width()+0.5, i.get_y() + 0.075, str(i.get_width()), fontsize=10, color='black')
   
        ax.set_xlim(0, 25)
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.set_title('Type of AustLit data for each DAAO-KMN artist')

        cols = st.columns(2)
        with cols[0]:
                st.write(f"**What type of data is available for each artist in AustLit?**") 
                st.pyplot(fig)
        with cols[1]:
                st.write("**Data defintions:**")
                expander_labels = ["agentWorksBy", "agentWorksAbout", "agentWorksWorks", "AgentText_Awards"]
                selection = st.segmented_control(
                        " ",
                        options=expander_labels,
                        default=expander_labels[0],
                        label_visibility="hidden",
                        selection_mode="single",
                )
                if selection == expander_labels[0]:
                        st.image(f"images/austlit_worksby.png", caption="Example: Julie Dowling")
                elif selection == expander_labels[1]:
                        st.image(f"images/austlit_worksabout.png", caption="Example: Julie Dowling")
                elif selection == expander_labels[2]:
                        st.image(f"images/austlit_worksworks.png", caption="Example: Julie Dowling")
                elif selection == expander_labels[3]:
                        st.image(f"images/austlit_awards.png", caption="Example: Julie Dowling")
                else:
                        st.write("Select a data type to view its definition")

def generate_tab2():
        st.caption("""
                    - Who legitimates artists – function of critics, commentators (the change to online commentary)? 
                    - What is the relationship between the material that appears publicly in the ‘end point’ of 
                    the exhibition and the material on which the curatorial process draws? In other words, to 
                    create KMN exhibition? 
                    - Link between Anne Marsh entries (in the dataset) and material that appears in other collections
                    - Key words that constellate around women’s art criticism as they appear in the KMN critical book and 
                        cognate art/literary criticism  ")
                    - In what sense does ‘feminism’ represent white women? 
                """
        )

page3_dict = {
    'AustLit': generate_tab1,
    'Other': generate_tab2
}

def show():
        st.header("Art criticism and its impact on the KMN reception and legacy")

        tabs = st.tabs(list(page3_dict.keys()))
        for i, tab in enumerate(tabs):
                with tab:
                        page3_dict[list(page3_dict.keys())[i]]()