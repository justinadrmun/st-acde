import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from utils import (
        fetch_kmn_data, 
        fetch_archibald_participant_data,
        fetch_daao_kmn_related_people_records,
        fetch_daao_kmn_related_people,
        inspect_data
)
from custom_plot_funcs.archies_timeline import plot_timeline
from custom_plot_funcs.ratio_scatterplots import plot_male_relations, plot_female_relations

######## DAAO Intersection Overview ########
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
        frame = params['frame']
        frame = frame[frame["Collective/Individual"] == "Individual"]
        at_least_one_relation_sum = frame[frame['related_events'].notnull() | 
                                               frame['related_people'].notnull() | 
                                               frame['related_places'].notnull() | 
                                               frame['related_recognitions'].notnull() | 
                                               frame['related_resources'].notnull() | 
                                               frame['related_works'].notnull()].shape[0]

        st.write(f"**KMN (individual) artists with DAAO relations (n={at_least_one_relation_sum}):**")

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

######## Selected 5 artists ########
def generate_tab2(params):
        st.write("""
                Some kind of visualisation where we have, say, 5 artists from the KMN collection, with a 
                little panel of 5 items of metadata about them (a line could then link out to a photograph 
                of one of their exhibition artworks)
                 """
        )

######## Archibald ########
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
        st.write(f"**KMN Artists who have participated in the Archibald Prize (n={found_participants.found.nunique()}):**")
        cols = st.columns([1, 5, 1])
        with cols[1]:
                plot_timeline()
        with cols[0]:
                if st.button("Inspect data :mag_right:", key="archibald"):
                        inspect_data(found_participants)
        
######## DAAO Relation Deep Dive ########
def generate_tab4(params):
        st.caption("""
                 Data imagery – who is included/ relationship to DAAO, gender differences, geographic spread, date range for birth of subjects?
                """)

        st.divider()
        columns = st.columns([0.7, 0.3])

        with columns[0]:
                related_records = fetch_daao_kmn_related_people_records(v2=True)
                st.write(f"**Predicate type of DAAO people relations (n={related_records.shape[0]}):**")
                st.caption("Predicate types are the types of relationships between a given KMN artist and related person in the DAAO.")
                if st.button("Inspect data :mag_right:", key="daao_relations"):
                        inspect_data(related_records)  
                st.bar_chart(related_records["predicate"].value_counts(), horizontal=True)
                
        with columns[1]:
                daao_related_people = fetch_daao_kmn_related_people(v2=True)
                st.write(f"**Gender distribution of DAAO related people (n={daao_related_people.shape[0]}):**")
                st.caption("This data consists of all the people records in the DAAO who are related to KMN artists.")
                if st.button("Inspect data :mag_right:", key="daao_related_people"):
                        inspect_data(daao_related_people)  

                fig, ax = plt.subplots()
                daao_related_people["gender"].value_counts().plot.pie(autopct='%1.1f%%', ax=ax)
                ax.set_ylabel("")
                ax.set_xlabel("")
                st.pyplot(fig)
        
        st.divider()
        # count the number of unique related_records["gender"] values for each unique related_records["Artist"]
        props = pd.crosstab(related_records["Artist"], related_records["gender"], normalize="index")
        counts = pd.crosstab(related_records["Artist"], related_records["gender"], margins=True)
        summary = counts.merge(props, left_index=True, right_index=True, suffixes=('_count', '_proportion'))
        summary.reset_index(inplace=True)
        summary = summary.merge(related_records[["Artist","Link to DAAO"]].drop_duplicates(), on="Artist", how="inner")
        summary = summary.merge(fetch_kmn_data(v2=True)[["Link to DAAO", "Year of Birth"]], on="Link to DAAO", how="inner")

        # show missing values for year of birth
        summary = summary[summary['Year of Birth'].notnull()]

        # most values are integers, but some are strings i.e., '1887 or 1885'
        summary['Year of Birth'] = summary['Year of Birth'].str.extract(r'(\d{4})').astype(int)

        # create a vicennium birth year column
        summary["decade_birth_year"] = (summary["Year of Birth"] // 10) * 10

        columns = st.columns(3)
        with columns[0]:
                st.write("**Frequency of related person records by gender?**")
                all_mean = str(round(summary["All"].mean(),2))
                all_median = str(round(summary["All"].median(),2))
                st.metric(label="No. of KMN artists with DAAO related person records", value=str(summary.shape[0]))
                
                # identify the person with the most related person records
                max_related = summary["All"].idxmax()
                st.metric(label="Most related person records (Thea Proctor)", 
                          value=summary.loc[max_related, "All"])

                st.metric(label="Mean no. of related person records", value=all_mean)
                st.metric(label="Median no. of related person records", value=all_median)

        with columns[1]:
                # generate bar plot for the number of related person records per artist
                bin_conds = {
                                "1 relation": summary["All"] == 1,
                                "2-4 relations": summary["All"].between(2, 4, inclusive="both"),
                                "5-9 relations": summary["All"].between(5, 9, inclusive="both"),
                                "10+ relations": summary["All"] >= 10
                }

                summary["Bin"] = np.where(bin_conds["1 relation"], "1 relation",
                                np.where(bin_conds["2-4 relations"], "2-4 relations",
                                np.where(bin_conds["5-9 relations"], "5-9 relations",
                                np.where(bin_conds["10+ relations"], "10+ relations", "Other"))))
                
                fig, ax = plt.subplots()
                ax.bar(bin_conds.keys(), [summary[cond]["All"].value_counts().sum() for cond in bin_conds.values()])
                # add proportion, not sum labels
                for i, v in enumerate([summary[cond]["All"].value_counts().sum() for cond in bin_conds.values()]):
                        ax.text(i, v + 0.5, str(round(v/summary.shape[0]*100, 2)) + "%", ha='center')
                ax.set_title('Number of KMN Artists per $\it{n}$ number of \nrelated person records in DAAO')
                # increase y limits 
                ax.set_ylim(0, 50)
                st.pyplot(fig)
                st.caption("18% of KMN artists (found in the DAAO) have 10 or more links with other people in the DAAO.")
        
        with columns[2]:
                mean_proportions = summary.groupby('Bin')[['"male"_proportion', '"female"_proportion']].mean()\
                        .rename(columns={
                                "\"male\"_proportion": "Average Male Proportion", 
                                "\"female\"_proportion": "Average Female Proportion"})\
                        .reset_index()\
                        .set_index('Bin')

                fig, ax = plt.subplots()
                mean_proportions = mean_proportions.loc[list(bin_conds.keys())].reset_index()
                mean_proportions.plot(kind='bar', x='Bin', ax=ax, 
                                      stacked=False, rot=0, color=['tab:orange', 'tab:blue'])

                # set x-axis title
                ax.set_xlabel("")
                ax.set_title('Average proportion of person records in DAAO, Male and Female\n\n')

                # increase y limit
                ax.set_ylim(0, 0.65)

                # move legend to the top of the plot
                ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=2)
                st.pyplot(fig)
                st.caption("Most links with other people in the DAAO are female.")

        st.divider()
        columns = st.columns([0.3,1,1])
        with columns[1]:
                st.write("**KMN artists with more than double male relations in the DAAO**")
                more_than_double_male_relations = summary[(summary['"male"_proportion'] > 0.66) & 
                                                        (summary['All'] > 4)]\
                                                .sort_values(by='"male"_proportion', ascending=False)\
                                                .reset_index(drop=True)
                plot_male_relations(more_than_double_male_relations)
        with columns[2]:
                st.write("**KMN artists with more than double female relations in the DAAO**")
                more_than_double_female_relations = summary[(summary['"female"_proportion'] > 0.66) & 
                                                (summary['All'] > 4)]\
                                        .sort_values(by='"female"_proportion', ascending=False)\
                                        .reset_index(drop=True)
                plot_female_relations(more_than_double_female_relations)    
        with columns[0]:
                if st.button("Inspect data :mag_right:", key="daao"):
                        inspect_data(summary)  
                 
        st.divider()
        st.write("**Gender relation proportions over time**")
        st.caption('''
                   This plot checks to see whether the proportion of related records in the DAAO is changing over time.
                   For example, has there been a shift in the type of networks over time?

                   We use date of birth as a proxy for time, as this is the most populated data in the dataset. However,
                   this is not an accurate measure of artist activity.
                   '''
        )
                   
        by_birth_year = summary.groupby("decade_birth_year")[['"male"_proportion','"female"_proportion']].mean()
        by_birth_year.rename(columns={'"male"_proportion': "Average male proportion",
                                      '"female"_proportion': "Average female proportion",
                                          }, inplace=True)
        # remove the first row
        by_birth_year2 = by_birth_year
        # by_birth_year2 = by_birth_year.iloc[1:]

        fig, ax = plt.subplots(figsize=(16, 4))
        ax.axhline(y=0.5, color='grey', linestyle='dashed', lw=2, alpha=0.5)
        # add line plot with markers
        by_birth_year2.plot(kind='line', ax=ax, rot=0, color=['tab:orange', 'tab:blue'], marker='o')
      
        ax.set_title("")
        ax.set_xlabel("\nYear of birth of KMN artist (n = number of relations)")
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=2)

        # show each decade on the x-axis
        ax.set_xticks(by_birth_year2.index)
        ax.set_xticklabels(
                [f"{int(year)} \n(n={int(summary[summary['decade_birth_year'] == year]["All"].sum())})" 
                 for year in by_birth_year.index])
                  
        columns = st.columns([2.5, 0.5])
        with columns[0]:
                st.pyplot(fig)
                     
        
def generate_tab5(params):
        st.caption("""
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
        kmn = fetch_kmn_data(v2=True)
        params = {'frame': kmn}

        tabs = st.tabs(list(page1_dict.keys()))
        for i, tab in enumerate(tabs):
                with tab:
                        page1_dict[list(page1_dict.keys())[i]](params)