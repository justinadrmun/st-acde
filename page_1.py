import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from utils import (
        fetch_kmn_data, 
        fetch_archibald_participant_data,
        fetch_daao_kmn_related_people_records,
        fetch_daao_kmn_related_people
)
from custom_plot_funcs.archies_timeline import plot_timeline

def generate_tab1(params):
        st.caption("""
                 Some kind of visualisation showing the ‘Top 10’ artists in the collection by way of how ‘visible’ 
                 they are in existing cultural databases. i.e. who from the KMN dataset appears the most in DAAO and Prints & Printmaking?
                 """
        )
        frame = params['frame']
        frame = frame[["Artist"] + [col for col in frame.columns if 'Link' in col]]
        frame["count"] = frame.count(axis=1)
        frame = frame.sort_values('count', ascending=False)
        visible_artists = frame[frame['count'] == frame['count'].max()]["Artist"].values
        st.write(f"**Artists that exist in DAAO, AWR and NLA (n={len(visible_artists)}):**")
        cols = st.columns(5)
        for idx, artist in enumerate(visible_artists):
                with cols[idx % 5]:
                        st.metric(value="", label=artist)

        st.divider()
        st.write(f"**KMN artists with DAAO relations:**")
        frame = params['frame']
        frame = frame[frame["Collective/Individual"] == "Individual"]

        categories = [
        ("Most related event records", 'related_events'),
        ("Most related people records", 'related_people'),
        ("Most related place records", 'related_places'),
        ("Most related recognition records", 'related_recognitions'),
        ("Most related resource records", 'related_resources'),
        ("Most related work records", 'related_works')
        ]

        for i in range(0, len(categories), 3):
                col1, col2, col3 = st.columns(3)
                for col, (title, column) in zip([col1, col2, col3], categories[i:i+3]):
                        with col:
                                st.write(title)
                                st.bar_chart(frame[['Artist', column]]
                                             .sort_values(by=column, ascending=False)
                                             .head(10).set_index('Artist'), horizontal=True)

def generate_tab2(params):
        st.write("""
                Some kind of visualisation where we have, say, 5 artists from the KMN collection, with a 
                little panel of 5 items of metadata about them (a line could then link out to a photograph 
                of one of their exhibition artworks)
                 """
        )

def generate_tab3(params):
        st.caption("""
                 KMN meets Archibald – data viz overview. Show women in the Archibald who also feature in KMN.
                 """
        )
        found_participants = fetch_archibald_participant_data(filter="kmn")
        winners = found_participants[
                        found_participants['3']\
                                .str.contains('Winner', na=False)][["1","2","3","Year"]]\
                                .rename(columns={"1":"KMN Artist", "2":"Title", "3":"Prize"})\
                                .sort_values(by="Year", ascending=True)
        st.write(f"**KMN Artists who have won the Archibald Prize:**")
        for rows in [winners[:4].iterrows(), winners[4:].iterrows()]:
                cols = st.columns(4)

                for i, (_, row) in enumerate(rows):
                        with cols[i % 4]:
                                st.metric(label=str(row["Year"]), value=row["KMN Artist"])
                                st.image(f"images/archies_{str(row['Year'])}.jpg", caption=row["Title"])
        st.divider()
        st.write(f"**KMN Artists who have participated in the Archibald Prize:**")
        _, col2, _ = st.columns([1, 5, 1])
        with col2:
                plot_timeline()

def generate_tab4(params):
        st.caption("""
                 Data imagery – who is included/ relationship to DAAO, gender differences, geographic spread, date range for birth of subjects?
                """)

        st.divider()
        columns = st.columns([0.7, 0.3])

        with columns[0]:
                st.write("**Predicate type of DAAO people relations**")
                related_records = fetch_daao_kmn_related_people_records()
                st.bar_chart(related_records["predicate"].value_counts(), horizontal=True)
                
        with columns[1]:
                st.write("**Gender distribution of DAAO related people**")
                daao_related_people = fetch_daao_kmn_related_people()

                fig, ax = plt.subplots()
                daao_related_people["gender"].value_counts().plot.pie(autopct='%1.1f%%', ax=ax)
                ax.set_ylabel("")
                ax.set_xlabel("")
                st.pyplot(fig)

        
def generate_tab5(params):
        st.markdown("""
                 - Compare with data from Australia exhibition at Royal Academy in 2013 
                 - Rex Butler – decrying the lack of artistic judgment that data-driven/metric-based merit shows have on the discipline of art history 
                 - What happens when you datafy (or reverse engineer as data) an exhibition that happened in situ?
                    """
        )

page1_dict = {
    'Top 10': generate_tab1,
    '5 Artists': generate_tab2,
    'Archibald': generate_tab3,
    'DAAO': generate_tab4,
    'Other': generate_tab5
}

def show():
        st.header("Data comparisons")
        kmn = fetch_kmn_data()
        params = {'frame': kmn}

        tabs = st.tabs(list(page1_dict.keys()))
        for i, tab in enumerate(tabs):
                with tab:
                        page1_dict[list(page1_dict.keys())[i]](params)