import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from utils import fetch_kmn_data, fetch_kmn_artists_exhibitions
from custom_plot_funcs.population_pyramid import population_pyramid

import pycountry_convert as pc

def country_to_continent(country_name):
        country_alpha2 = pc.country_name_to_country_alpha2(country_name)
        country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
        country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
        return country_continent_name

NEW_COLS: list = [
        # 'event_date',
        'place.address.country', # country of venue of venue id related to new_venue_name_y
        'artist', # kmn artist name
        'artist_ori_dbid', # kmn artist oid
        'ori_dbid', # chosen venue id, if null this means not a chosen venue
        'no_of_events', # no of events if venue id is related to chosen venue, many venue ids represent the same entity
        'total_no_of_events', # no of total events, aggregated event count of distinct venues
        'new_venue_name_y', # distinct venues, venue name we go with hereonin
        'venue_name', # venue name of venue id related to new_venue_name_y
        'venue_category_minor', # minor category of new_venue_name_y according to Scott East
        'venue_category_major', # major category of new_venue_name_y according to Scott East
        'State' # state of new_venue_name_y according to Scott East
]

# get raw exhibition data with aggregated venue data for categorisation purposes
kmn_artists_exhibitions = fetch_kmn_artists_exhibitions()[NEW_COLS]

# we use this cond to represent "large galleries", national institution relates to National Gallery
kmn_artists_exhibitions["is_large_gallery"] = np.where(kmn_artists_exhibitions.venue_category_minor.isin(
["National Institution", "State Gallery / Library"]), True, False)

# we use this cond to represent "regional galleries", regional institution relates to regional galleries
kmn_artists_exhibitions["is_regional_gallery"] = np.where(kmn_artists_exhibitions.venue_category_minor.isin(
["Local Government and/or Regional Gallery"]), True, False)


def generate_tab1():
        # get unique large galleries
        large_galleries = kmn_artists_exhibitions[kmn_artists_exhibitions["is_large_gallery"]].value_counts("new_venue_name_y").reset_index()
        large_galleries_frame = pd.DataFrame(large_galleries)
        large_galleries_frame = large_galleries_frame.rename(columns={0: "count"})
        large_galleries_frame = large_galleries_frame.merge(kmn_artists_exhibitions[["new_venue_name_y", "venue_category_minor"]], on="new_venue_name_y").drop_duplicates()
        large_galleries_frame.columns = ["Major galleries", "Count", "Venue Category Minor"]

        st.caption("""
                    Have all of the KMN women had their work exhibited in a ‘major’ Australian gallery? In 
                    other words, in putting the KMN list together, was a curatorial decision made (either 
                    explicitly or indirectly) about the connection between significance of an artist and where 
                    their work was shown? 
                 """
        )

        st.subheader(f"**Analysing artists who have exhibited in major galleries**")
        url = "https://acd-engine.github.io/jupyterbook/Analysis_DAAOVenues.html#final-cleaning-phase-and-removing-duplicates"
        st.write("""
                 1. We first identify every artist in the KMN dataset who has participated in an exhibition according to the DAAO"
                 2. Using categorisation from [Scott East's list of 119 venues](%s), 
                        we identify major galleries as venues labelled as *National Institution* and *State Gallery / Library*.
                 """ % url)
        st.warning("Please note that participation frequency in the visuals below are not filtered on events with dates, which differs with the analysis in the link above.",
                   icon="⚠️")
        
        frame_cols = st.columns([2.25, 1])
        # determine height of dataframe based on number of rows
        numRows = large_galleries_frame.shape[0]
        with frame_cols[0]:
                st.dataframe(large_galleries_frame[["Major galleries", "Venue Category Minor", "Count"]], 
                        hide_index=True,
                        use_container_width=True,
                        height=(numRows + 1) * 35 + 3,
                        column_config={
                                "Count": st.column_config.ProgressColumn(
                                        "No. of exhibition participations by KMN artists",
                                        format="%s",
                                        min_value=0,
                                        max_value=int(large_galleries_frame["Count"].max())
                                )
                        }, 
                )
        st.write(
                """
                3. Lastly, we count and visualise the number and percentage of major gallery exhibitions for each KMN artist in relation to their total number of exhibitions.
                """
        )

        st.divider()
        # groupby count of large_galleries for evey artist, number when is_large_gallery is 1 and when is_large_gallery is 0
        # sum = number of events in a large gallery
        # count = number of events in total
        large_gallery_count = kmn_artists_exhibitions.groupby("artist")\
        .agg({"is_large_gallery": ["sum", "count"]})\
        .sort_values(by=('is_large_gallery', 'count'), ascending=False).reset_index()

        # create percentage column, to understand 
        large_gallery_count["events_in_large_gallery_%"] = (
        large_gallery_count[
                ('is_large_gallery', 'sum')] / large_gallery_count[
                ('is_large_gallery', 'count')])  * 100
        
        no_large_galleries_cnt = large_gallery_count[large_gallery_count["events_in_large_gallery_%"] == 0]
        no_large_galleries_perc = round((no_large_galleries_cnt.shape[0]/large_gallery_count.shape[0]) * 100,2)

        # scatter plot of percentage of exhibitions in large galleries vs number of exhibitions
        fig, ax = plt.subplots()
        sns.scatterplot(data=large_gallery_count, y='events_in_large_gallery_%', x=('is_large_gallery', 'count'))
        plt.xlabel('Number of exhibitions (in DAAO) by a given KMN artist')
        plt.ylabel('Percentage of exhibitions in major galleries')

        # change colour of data points of artists who have not exhibited in a major gallery 
        for i, row in no_large_galleries_cnt.iterrows():
                plt.scatter(
                        row[('is_large_gallery', 'count')], 
                        row['events_in_large_gallery_%'], 
                        color='tab:orange',
                        # change border colour to white
                        edgecolors='white',
                        linewidths=0.2

                )
        
        # add legend for the scatter plot
        plt.legend(['Artists with major gallery participations', 'Artists with NO major gallery participations'])
        
        # add an annotation to the plot to indicate that the outlier is the artist with the most exhibitions
        max_exhibitions = large_gallery_count[('is_large_gallery', 'count')].max()
        max_perc = large_gallery_count[large_gallery_count[('is_large_gallery', 'count')] == max_exhibitions]['events_in_large_gallery_%'].values[0]
        plt.annotate(
                "Gwyn Piggott",
                xy=(max_exhibitions, max_perc),
                xytext=(max_exhibitions-40, max_perc+5),
        )
     
        columns = st.columns([0.75,0.5,0.75], gap="medium")
        with columns[0]:
                st.write('Exhibition count vs percentage of exhibitions in large galleries')
                st.pyplot(fig)
        with columns[1]:
                no_large_galleries_cnt.columns = no_large_galleries_cnt.columns.droplevel(1)
                no_large_galleries_cnt.columns = ['KMN Artist', 'No. of major galleries exhibitions','No. of exhibitions (total)', '(%)']
                no_large_galleries_cnt.drop(columns=['(%)'], inplace=True)

                st.write("")
                st.write("")
                st.write(f"Out of the KMN artists who have DAAO exhibition data ({large_gallery_count.shape[0]}), there are")
                metric_cols1 = st.columns(2)
                with metric_cols1[0]:
                        st.metric("metric1", f"{no_large_galleries_cnt.shape[0]} artists", label_visibility="collapsed")
                st.caption("with **no** exhibitions in large galleries, amounting to")
                metric_cols2 = st.columns(2)
                with metric_cols2[0]:
                        st.metric("metric2", f"{no_large_galleries_perc} %", label_visibility="collapsed")
                st.caption("of all KMN artists with DAAO exhibition data.")
        with columns[2]:
                st.write("")
                st.write("")
                with st.expander("Expand to see artists:"):
                        st.dataframe(no_large_galleries_cnt, hide_index=True, use_container_width=True)


def generate_tab2():
        st.caption("""
                    TLCMap to show whether KMN involved a deceptive geographical spread; distinguishes 
                    Indigenous artists from urban artists 
                 """
        )
        st.subheader(f"**Map of artists' birthplaces, Indigenous artists vs urban artists:**")
        st.write("")
        space_cols = st.columns([0.01,1])
        with space_cols[1]:
                st.write(f":large_orange_circle: = indigenous artists | :large_blue_circle: = non-indigenous artists")
        kmn = fetch_kmn_data()
        indigenous = "First Nations People Group (from Know My Name only)"
        # if indigenous col is null then make colour #0044ff, else #FF0000
        kmn["color"] = kmn[indigenous].apply(lambda x: "#1f77b4" if pd.isnull(x) else "#ff7f0e")
        all_country_toggle = st.toggle("Show all country data", False)

        if all_country_toggle:
                st.map(kmn[["Artist","Country of Birth","Place of Birth Longitude", "Place of Birth Latitude","color"]]\
                .dropna()\
                .rename(
                        columns={"Place of Birth Latitude": "lat", 
                                "Place of Birth Longitude": "lon"}),
                        color="color",
                        zoom=1
                        )
        else:
                australia = kmn["Country of Birth"] == "Australia"
                st.map(kmn[australia][["Artist","Country of Birth","Place of Birth Longitude", "Place of Birth Latitude","color"]]\
                .dropna()\
                .rename(
                        columns={"Place of Birth Latitude": "lat", 
                                "Place of Birth Longitude": "lon"}),
                        color="color",
                        zoom=3
                        )

def generate_tab3():
        st.caption("""
                    International mobilities – might we show some artists on a map who have also moved 
                    and worked/exhibited beyond Australia
                 """
        )

        st.subheader(f"**International mobilities:**")
        st.write("Analysing summary statistics of the number of exhibitions (DAAO) in countries other than Australia")
                 
        # find the artists with the higher count the number of non-Australian countries of the column : place.address.country
        international_mobilities_count = kmn_artists_exhibitions[["artist","place.address.country"]][kmn_artists_exhibitions["place.address.country"].notnull()]
        international_mobilities_frame = kmn_artists_exhibitions[["artist","place.address.country"]][kmn_artists_exhibitions["place.address.country"].notnull()]

        # create new Australia indicator column
        international_mobilities_count["is_international"] = np.where(international_mobilities_count["place.address.country"] != "Australia", 1, 0)
        international_mobilities_count["is_local"] = np.where(international_mobilities_count["place.address.country"] == "Australia", 1, 0)        

        # group by artist and count the number of unique countries
        international_mobilities_count = international_mobilities_count.groupby("artist")\
        .agg({"place.address.country": "nunique", "is_international": "sum", "is_local": "sum"})\
        .reset_index()\
        .rename(columns={"place.address.country": "no_of_countries", "is_international": "is_international", "is_local": "is_local"})
        
        # add percentage column of is_international to is_international + is_local
        international_mobilities_count["countries_%"] = round(
                (international_mobilities_count["is_international"] / (international_mobilities_count["is_international"] + international_mobilities_count["is_local"])) * 100, 2)
        
        international_mobilities_count["no_of_countries"] = international_mobilities_count["no_of_countries"] - 1

        # rearrange columns
        international_mobilities_count = international_mobilities_count[["artist", "is_international", "no_of_countries","countries_%"]]

        # international_mobilities_count contains the number of international exhibitions, number of unique international countries, percentage of international to total exhibition participations
        # it is missing a unique list of participated countries for each artist
        # create a new column in international_mobilities_count with the list of countries, must be a list
        international_mobilities_count["Countries"] = international_mobilities_count["artist"].apply(
                lambda x: international_mobilities_frame[international_mobilities_frame["artist"] == x]["place.address.country"].unique().tolist()
        )

        # remove Australia from the list of countries
        international_mobilities_count["Countries"] = international_mobilities_count["Countries"].apply(
                lambda x: [i for i in x if i != "Australia"]
        )

        international_mobilities_count.columns = [
                "KMN Artist", "No. of international exhibitions", "No. countries", "% of international to total exhibition participations","Countries"
        ]
        international_mobilities_count = international_mobilities_count[[ "KMN Artist", "No. of international exhibitions", "Countries","% of international to total exhibition participations"]]
        numRows = 15

        column_config_dict = {}
        for cols in ["No. of international exhibitions", "% of international to total exhibition participations"]:
                column_config_dict[cols] = st.column_config.ProgressColumn(
                        cols,
                        format="%s",
                        min_value=0,
                        max_value=int(international_mobilities_count[cols].max()) if isinstance(international_mobilities_count[cols], int) else 100
                )
        
        st.dataframe(international_mobilities_count.sort_values("% of international to total exhibition participations", ascending=False),
                        hide_index=True,
                        use_container_width=True,
                        height=(numRows + 1) * 35 + 3,
                        column_config=column_config_dict, 
        )

        st.divider()
        st.write("International exhibition participation by continent")
        international_mobilities_frame["continent"] = international_mobilities_frame["place.address.country"].apply(lambda x: country_to_continent(x))
        international_mobilities_frame = international_mobilities_frame[international_mobilities_frame["place.address.country"] != "Australia"]
        st.bar_chart(international_mobilities_frame["continent"].value_counts(), horizontal=True)

        # find artists with the most continents
        most_continents = international_mobilities_frame.groupby("artist")\
        .agg({"continent": "nunique"})\
        .sort_values(by="continent", ascending=False).reset_index()

        most_continents.columns = ["KMN Artist", "No. of unique continents"]
        most_continents = most_continents[most_continents["No. of unique continents"] >= 3]

        # add column with list of continents
        most_continents["Continents"] = most_continents["KMN Artist"].apply(lambda x: international_mobilities_frame[international_mobilities_frame["artist"] == x]["continent"].unique())

        st.write("Artists with international exhibitions, most unique continents (n > 2):")
        st.dataframe(most_continents[["KMN Artist", "Continents"]], hide_index=True, use_container_width=True, height=(most_continents.shape[0] + 1) * 35 + 3)

def generate_tab4():
        st.caption("Could we visualize those in KMN who had work shown in major galleries vs regional (minor galleries)")

        st.subheader(f"**Major vs Regional Galleries**")
        st.write("""
                        1. We first identify every artist in the KMN dataset who has participated in an exhibition according to the DAAO.
                        2. Using categorisation from [Scott East's list of 119 venues](https://acd-engine.github.io/jupyterbook/Analysis_DAAOVenues.html#final-cleaning-phase-and-removing-duplicates), we identify major galleries as venues labelled as *National Institution* and *State Gallery / Library*.
                        3. We then identify regional galleries as venues labelled as *Local Government and/or Regional Gallery*.
                        4. We then count and visualise the number of major and regional gallery exhibition participations for each KMN artist.    
                """
        )
        st.warning("Please note that participation frequency in the visuals below are not filtered on events with dates, which differs with the analysis in the link above.",
                   icon="⚠️")
        
        # keep data where is_large_gallery is True or False, or is_regional_gallery is True or False
        major_vs_regional = kmn_artists_exhibitions[
                (kmn_artists_exhibitions["is_large_gallery"]) | (kmn_artists_exhibitions["is_regional_gallery"])
        ]

        # sorted by sum of large galleries
        major_vs_regional_sort_by_major_count = major_vs_regional.groupby("artist")\
        .agg({"is_large_gallery": ["sum"], "is_regional_gallery": ["sum", "count"]})\
        .sort_values(by=[('is_large_gallery', 'sum'),('is_regional_gallery', 'sum')], ascending=False).reset_index()

        major_vs_regional_sort_by_major_count.columns = [
                "artist", "is_large_gallery","is_regional_gallery", "total"]

        # sorted by sum of regional galleries
        major_vs_regional_sort_by_reg_count = major_vs_regional.groupby("artist")\
        .agg({"is_large_gallery": ["sum"], "is_regional_gallery": ["sum", "count"]})\
        .sort_values(by=[('is_regional_gallery', 'sum'),('is_large_gallery', 'sum')], ascending=False).reset_index()

        major_vs_regional_sort_by_reg_count.columns = [
                "artist", "is_large_gallery","is_regional_gallery", "total"]

        st.divider()
        major_vs_regional_toggle = st.toggle("Sort plot below by major galleries for different view", False)

        major_vs_reg_cols = st.columns([2,1], gap="medium")

        with major_vs_reg_cols[0]:
                if  major_vs_regional_toggle:
                        st.pyplot(population_pyramid(major_vs_regional_sort_by_major_count, remove_yticks=True))
                else:
                        st.pyplot(population_pyramid(major_vs_regional_sort_by_reg_count, remove_yticks=True))
        
        with major_vs_reg_cols[1]:
                # top 5 artists with most major gallery exhibitions
                st.write("Top 5 artists with the most **major** gallery exhibitions:")
                top_5_major = major_vs_regional_sort_by_major_count.head(5)
                st.pyplot(population_pyramid(top_5_major, remove_yticks=False))

                # top 5 artists with most regional gallery exhibitions
                st.write("Top 5 artists with the most **regional** gallery exhibitions:")
                top_5_regional = major_vs_regional_sort_by_reg_count.head(5)
                st.pyplot(population_pyramid(top_5_regional, remove_yticks=False))

        st.divider()
        st.write("KMN artists with participations with regional galleries, but no major galleries:")
        regional_no_major = major_vs_regional_sort_by_reg_count[
                (major_vs_regional_sort_by_reg_count["is_large_gallery"] == 0) & 
                (major_vs_regional_sort_by_reg_count["is_regional_gallery"] > 0)
        ]
        st.dataframe(regional_no_major, hide_index=True, use_container_width=True)
        

        
def generate_tab5():
       st.caption("""
                    - Can we map the locality/relations of collective arts practices where they are explicitly identified in KMN – away from individuation of authorship.
                    - Social media representations
                """
       )

page5_dict = {
    "Major Galleries": generate_tab1,
    "TLCMap": generate_tab2,
    "International Mobilities": generate_tab3,
    "Major vs Regional": generate_tab4,
    "Other": generate_tab5,
}

def show():
        st.header("The Boundaries of Experience")

        tabs = st.tabs(list(page5_dict.keys()))
        for i, tab in enumerate(tabs):
                with tab:
                        page5_dict[list(page5_dict.keys())[i]]()