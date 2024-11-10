import streamlit as st
import pandas as pd
import numpy as np
from utils import fetch_kmn_data

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
        ("Most related events", 'related_events'),
        ("Most related people", 'related_people'),
        ("Most related places", 'related_places'),
        ("Most related recognitions", 'related_recognitions'),
        ("Most related resources", 'related_resources'),
        ("Most related works", 'related_works')
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
        st.markdown("""
                 - KMN meets Archibald – data viz overview.
                 - Show women in the Archibald who also feature in KMN
                 """
        )

def generate_tab4(params):
        st.write("""
                 Data imagery – who is included/ relationship to DAAO, gender differences, geographic spread, date range for birth of subjects?
                """)
        
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