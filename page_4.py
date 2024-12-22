import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_timeline import timeline
from collections import defaultdict
import seaborn as sns
import ast

from utils import (
    fetch_daao_kmn_related_people_records, 
    fetch_daao_kmn_related_people_withcount,
    fetch_daao_recognised_individuals
)

def generate_tab1():
        st.caption("""
                    Is it possible to trace the distinction/relation between women in KMN who had a partner 
                    that was evidently impactful in terms of their networks and/or career and those who also 
                    had (or just had) a collaborator of some kind; a double act, mutually-enabling 
                    partnership? 
                 """
        )
        frame = fetch_daao_kmn_related_people_withcount()
        frame_records = fetch_daao_kmn_related_people_records()

        st.write(f"**Legend for network graphs:**")
        space_cols = st.columns([0.01,1])
        with space_cols[1]:
                st.write(f":large_green_circle: = KMN individuals | :large_orange_circle: = KMN-related male in DAAO | :large_blue_circle: = KMN-related female in DAAO")

        with st.expander("Influential nodes based on intersecting related people across KMN dataset", expanded=True):
                cols = st.columns([1,1.1])
                with cols[0]:
                        st.caption("""
                                        1. We first identify every related person to individuals from the KMN dataset
                                        2. We check to see whether any related people exist for many KMN individuals
                                        3. We generate a network graph using only related people with at least 4 relations with KMN individuals
                                """
                        )

                        # get people with a count higher than 3
                        influential_nodes = frame_records.related_person_oid.value_counts().reset_index()
                        influential_nodes = influential_nodes[influential_nodes['count'] > 3]

                        fig, ax = plt.subplots()
                        influential_nodes_frame = frame[
                                frame.ori_dbid.isin(influential_nodes.related_person_oid)][["ori_dbid", "display_name"]]
                        pd.merge(influential_nodes_frame, 
                                 pd.DataFrame(influential_nodes), 
                                 left_on='ori_dbid', 
                                 right_on='related_person_oid', 
                                 how='left')\
                                .drop(["ori_dbid","related_person_oid"], axis=1)\
                                .sort_values(by='count', ascending=True)\
                                .plot(kind='barh', 
                                      x='display_name', 
                                      y='count', 
                                      ax=ax, 
                                      legend=False
                                )
                        # remove the x-axis label
                        plt.ylabel('')
                        st.pyplot(fig)
                        st.caption("People in the DAAO with the most number of relations with KMN individuals")
                with cols[1]:
                        st.image("images/networks/relatedpeople-intersect-network.png", 
                                 caption="Network graph of related people with at least 4 relations with KMN individuals")
                        
        with st.expander("Influential nodes based on related people with the highest number of **related events**"):
                cols = st.columns([1,1.1])
                with cols[0]:
                        st.caption("""
                                        1. We first identify every related person to individuals from the KMN dataset
                                        2. We calculate the count of related events related to each KMN-relation. This acts as a proxy for "influential".
                                        3. We generate a network graph of these "influential" nodes and the corresponding KMN artists
                                """
                        )

                        # get people with a count higher than 3
                        most_related_events = frame[frame.related_events >= 30].sort_values("related_events", ascending=True)
                        fig, ax = plt.subplots()
                        most_related_events\
                                .plot(kind='barh', 
                                      x='display_name', 
                                      y='related_events', 
                                      ax=ax, 
                                      legend=False
                                )
                        # remove the x-axis label
                        plt.ylabel('')
                        st.pyplot(fig)
                        st.caption("KMN-related individuals in the DAAO with the most number of related events")
                with cols[1]:
                        st.image("images/networks/mostrelatedevents-network.png", 
                                 caption="Network graph of KMN-related people with at least 30 related events. Values in brackets represent the number of related events")

        with st.expander("Influential nodes based on related people with the highest number of **related people**"):
                cols = st.columns([1,1.1])
                with cols[0]:
                        st.caption("""
                                        1. We first identify every related person to individuals from the KMN dataset
                                        2. We calculate the count of related people related to each KMN-relation. This acts as a proxy for "influential".
                                        3. We generate a network graph of these "influential" nodes and the corresponding KMN artists
                                """
                        )

                        # get people with a count higher than 3
                        most_related_people = frame[frame.related_people >= 23].sort_values("related_people", ascending=True)
                        fig, ax = plt.subplots()
                        most_related_people\
                                .plot(kind='barh', 
                                      x='display_name', 
                                      y='related_people', 
                                      ax=ax, 
                                      legend=False
                                )
                        # remove the x-axis label
                        plt.ylabel('')
                        st.pyplot(fig)
                        st.caption("KMN-related individuals in the DAAO with the most number of related people")
                with cols[1]:
                        st.image("images/networks/mostrelatedpeople-network.png", 
                                 caption="Network graph of KMN-related people with at least 23 related people. Values in brackets represent the number of related people")

        with st.expander("Influential nodes based on related people with the highest number of **related places**"):
                cols = st.columns([1,1.1])
                with cols[0]:
                        st.caption("""
                                        1. We first identify every related person to individuals from the KMN dataset
                                        2. We calculate the count of related places related to each KMN-relation. This acts as a proxy for "influential".
                                        3. We generate a network graph of these "influential" nodes and the corresponding KMN artists
                                """
                        )

                        # get people with a count higher than 3
                        most_related_places = frame[frame.related_places >= 15].sort_values("related_places", ascending=True)

                        fig, ax = plt.subplots()
                        most_related_places\
                                .plot(kind='barh', 
                                      x='display_name', 
                                      y='related_places', 
                                      ax=ax, 
                                      legend=False
                                )
                        # remove the x-axis label
                        plt.ylabel('')
                        st.pyplot(fig)
                        st.caption("KMN-related individuals in the DAAO with the most number of related places")
                with cols[1]:
                        st.image("images/networks/mostrelatedplaces-network.png", 
                                 caption="Network graph of KMN-related people with at least 15 related places. Values in brackets represent the number of related places")

        with st.expander("Influential nodes based on related people with the highest number of **related recogitions**"):
                cols = st.columns([1,1.1])
                with cols[0]:
                        st.caption("""
                                        1. We first identify every related person to individuals from the KMN dataset
                                        2. We calculate the count of related recogitions related to each KMN-relation. This acts as a proxy for "influential".
                                        3. We generate a network graph of these "influential" nodes and the corresponding KMN artists
                                """
                        )

                        # get people with a count higher than 3
                        most_related_recognitions = frame[frame.related_recognitions >= 7].sort_values("related_recognitions", ascending=True)

                        fig, ax = plt.subplots()
                        most_related_recognitions\
                                .plot(kind='barh', 
                                      x='display_name', 
                                      y='related_recognitions', 
                                      ax=ax, 
                                      legend=False
                                )
                        # remove the x-axis label
                        plt.ylabel('')
                        st.pyplot(fig)
                        st.caption("KMN-related individuals in the DAAO with the most number of related recognitions")
                with cols[1]:
                        st.image("images/networks/mostrelatedrecognitions-network.png", 
                                 caption="Network graph of KMN-related people with at least 7 related recognitions. Values in brackets represent the number of related recognitions")

        with st.expander("Influential nodes based on related people with the highest number of **related resources**"):
                cols = st.columns([1,1.1])
                with cols[0]:
                        st.caption("""
                                        1. We first identify every related person to individuals from the KMN dataset
                                        2. We calculate the count of related resources related to each KMN-relation. This acts as a proxy for "influential".
                                        3. We generate a network graph of these "influential" nodes and the corresponding KMN artists
                                """
                        )

                        # get people with a count higher than 3
                        most_related_resources = frame[frame.related_resources >= 21].sort_values("related_resources", ascending=True)

                        fig, ax = plt.subplots()
                        most_related_resources\
                                .plot(kind='barh', 
                                      x='display_name', 
                                      y='related_resources', 
                                      ax=ax, 
                                      legend=False
                                )
                        # remove the x-axis label
                        plt.ylabel('')
                        st.pyplot(fig)
                        st.caption("KMN-related individuals in the DAAO with the most number of related resources")
                with cols[1]:
                        st.image("images/networks/mostrelatedresources-network.png", 
                                 caption="Network graph of KMN-related people with at least 21 related resources. Values in brackets represent the number of related resources")

        with st.expander("Influential nodes based on related people with the highest number of **related works**"):
                cols = st.columns([1,1.1])
                with cols[0]:
                        st.caption("""
                                        1. We first identify every related person to individuals from the KMN dataset
                                        2. We calculate the count of related works related to each KMN-relation. This acts as a proxy for "influential".
                                        3. We generate a network graph of these "influential" nodes and the corresponding KMN artists
                                """
                        )

                        # get people with a count higher than 3
                        most_related_works = frame[frame.related_works >= 14].sort_values("related_works", ascending=True)

                        fig, ax = plt.subplots()
                        most_related_works\
                                .plot(kind='barh', 
                                      x='display_name', 
                                      y='related_works', 
                                      ax=ax, 
                                      legend=False
                                )
                        # remove the x-axis label
                        plt.ylabel('')
                        st.pyplot(fig)
                        st.caption("KMN-related individuals in the DAAO with the most number of related works")
                with cols[1]:
                        st.image("images/networks/mostrelatedworks-network.png", 
                                 caption="Network graph of KMN-related people with at least 14 related works. Values in brackets represent the number of related works")

def generate_tab2():
        st.caption("Marketplace analysis. Could we somehow showcase a few women from the exhibition who have the most ‘distinctive’ or ‘prestigious’ careers?")

        recognised_frame = fetch_daao_recognised_individuals()
        recognised_frame_withdates = recognised_frame[recognised_frame.year.notnull()]
        recognised_frame_withdates.display_name = recognised_frame_withdates.display_name.apply(lambda x: x.replace('"', ''))

        # add birth years
        birth_years = []
        for _, row in recognised_frame_withdates.iterrows():
                try:
                        birth_years.append(ast.literal_eval(row.birth)["coverage"]["date"]["year"])
                except:
                        birth_years.append(None)

        recognised_frame_withdates["birth_year"] = birth_years
        recognised_top9 = recognised_frame_withdates.display_name.value_counts().head(9).index
        recognised_top9_withdates = recognised_frame_withdates[recognised_frame_withdates.display_name.isin(recognised_top9)]
        recognised_top9_withdates["age_at_event"] = recognised_top9_withdates["year"] - recognised_top9_withdates["birth_year"].astype(int)

        # using age_at_event, calculate the number of events for each person every 10 years from 0 to 100
        age_bins = pd.cut(recognised_top9_withdates.age_at_event, bins=range(0, 110, 5), right=False)
        recognised_top9_withdates["age_bins"] = age_bins.astype(str)

        # pivot table, add suffix to display_name
        pivot = pd.pivot_table(recognised_top9_withdates, index="display_name", columns="age_bins", values="year", aggfunc="count", fill_value=0)
        pivot["total"] = pivot.sum(axis=1)
        pivot = pivot.sort_values("total", ascending=False)
        pivot = pivot.reset_index()
        pivot.columns.name = None
        pivot["display_name"] = pivot["display_name"] + " (" + pivot["total"].astype(str) + ")"
        pivot = pivot.set_index("display_name").drop("total", axis=1)

        fig, ax = plt.subplots(figsize=(6, 4))
        sns.heatmap(pivot, annot=True, fmt="d", cmap=sns.cubehelix_palette(as_cmap=True), ax=ax)
        plt.ylabel("")
        plt.xlabel("\nAge at recognition event")

        # flip the angle of the x-axis ticks
        plt.xticks(rotation=0, size=7)


        plt.title("")

        st.write(f"#### Number of recogniton events for each selected KMN individual")
        st.write("""
                 The heatmap shows the number of recognition events (i.e., awards in the DAAO) for a selection of KMN individual at different age brackets.
                 These KMN individuals were selected as they had at least 10 recognition events in the DAAO with temporal data. 
                 The values in the brackets represent the total number of recognition events for each individual.
                """
        )
        heatmap_cols = st.columns([1,5,1,1])
        with heatmap_cols[1]:
                st.pyplot(fig)

        st.divider()
        st.write(f"#### Explore the timeline of recognition events for each KMN individual")
        selection = st.segmented_control("placeholder", 
                                         recognised_top9, 
                                         selection_mode="single", 
                                         label_visibility="hidden", 
                                         default=recognised_top9[0])

        if selection:
                recognised_top9_withdates = recognised_top9_withdates[recognised_top9_withdates.display_name == selection]
                timeline_data = defaultdict(list)

                for _, row in recognised_top9_withdates.iterrows():
                        event = {
                                "start_date": {
                                "year": row.year
                                },
                                "text": {
                                "headline": row.label,
                                "text": f"[Age: {int(row.age_at_event)}] {row.description if pd.notnull(row.description) else ''}"
                                }
                        }
                        timeline_data["events"].append(event)

                timeline_data["title"] = {
                        "text": {
                                "headline": selection,
                                "text": f"No of recognition records = {recognised_top9_withdates.shape[0]} </p>"
                        }
                }

                timeline(timeline_data, height=400)  

        
def generate_tab3():
        st.caption("- Moving beyond the singular database – different identities as artists, e.g. Justin’s IMDB work etc.")

page4_dict = {
    'Partnerships': generate_tab1,
    'Marketplace': generate_tab2,
    'Other': generate_tab3
}

def show():
        st.header("Iconicity and Portfolio Careers")

        tabs = st.tabs(list(page4_dict.keys()))
        for i, tab in enumerate(tabs):
                with tab:
                        page4_dict[list(page4_dict.keys())[i]]()