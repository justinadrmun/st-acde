import pandas as pd
import streamlit as st
import numpy as np
import ast
import json
import warnings

def fetch_kmn_data():
    return pd.read_csv("data/kmn_with_related_data.csv")

def fetch_daao_kmn_data():
    return pd.read_csv("data/daao_kmn_individuals.csv")

def fetch_daao_kmn_alt_names():
    daao_frame = fetch_daao_kmn_data()
    alt_names = daao_frame[daao_frame["alternative_names"].notnull()][
        ["display_name", "primary_name", "alternative_names"]]
    
    alt_names_dict = dict()
    for _, alt_name in alt_names.iterrows():
        daao_name = alt_name.display_name.replace('"', '')
        a = ast.literal_eval(alt_name.alternative_names)
        alt_names_dict[daao_name] = []
        for display_name in a:
            if daao_name.strip() == display_name["display_name"].strip():
                continue
            alt_names_dict[daao_name].append(display_name["display_name"])

    # create a dataframe from alt_names_dict
    alt_names_frame = pd.DataFrame.from_dict( alt_names_dict, orient='index')\
            .reset_index()\
            .melt(id_vars='index', value_name='alternative_names')\
            .dropna()[["index","alternative_names"]]\
            .rename(columns={'index': 'display_name'})
    
    manual_categories = []
    with open('data/manual_alt_name_cats.txt', 'r') as f:
        [manual_categories.append(
            line.split('#')[0]\
                .replace('"', '')\
                .replace(',', '')\
                .strip()) 
                for line in f]
        
    alt_names_frame["category"] = manual_categories

    # remove Rearranged Names and Spacing
    alt_names_frame = alt_names_frame[~alt_names_frame["category"].isin(
        ["Rearranged Names", "Spacing"])]
    return alt_names_frame

def fetch_daao_kmn_related_people_records():
    kmn_frame = fetch_kmn_data() # KMN data
    daao_frame = fetch_daao_kmn_data() # DAAO data of KMN artists
    daao_related_people = fetch_daao_kmn_related_people() # related people according to DAAO, n=593

    # identify KMN artists with related people, n=142
    frame_related_people = kmn_frame[kmn_frame.related_people.notnull()]
    kmn_daao_links = frame_related_people[frame_related_people.related_people != 0]["Link to DAAO"].tolist()

    # for each KMN-DAAO match, fetch related people data
    related_records = pd.DataFrame()
    for daao_link in kmn_daao_links:
        this_artist = daao_frame[daao_frame["Link to DAAO"] == daao_link].iloc[0]
        data = pd.DataFrame(json.loads(str(this_artist["related_people"])))
        data["Artist"] = this_artist["display_name"]
        data["Link to DAAO"] = daao_link
        related_records = pd.concat([related_records, data])

    # add predicate column
    predicate = []
    related_person_oid = []
    for _,row in related_records.iterrows():
        if row["subject"]["label"] == row["Artist"].replace('"', ''):
            predicate.append(row.get("predicate", {}).get("term", "associate of"))
            related_person_oid.append(row["object"].get("ori_dbid", {}).get("$oid", np.nan))
        else:
            predicate.append(row.get("predicate", {}).get("reverse_term", "associate of"))
            related_person_oid.append(row["subject"].get("ori_dbid", {}).get("$oid", np.nan))

    related_records["predicate"] = predicate
    related_records["related_person_oid"] = related_person_oid

    daao_related_people_gender = daao_related_people[["gender", "ori_dbid"]].copy()
    daao_related_people_gender["ori_dbid"] = daao_related_people_gender["ori_dbid"]\
        .apply(lambda x: ast.literal_eval(x)["$oid"])

    # append gender information to related records
    related_records = related_records.merge(daao_related_people_gender, left_on='related_person_oid', right_on='ori_dbid', how='inner')
    return related_records.drop(columns=['ori_dbid'])

def fetch_daao_kmn_related_people():
    '''Fetch DAAO data of related people (according to DAAO) to KMN artists'''
    return pd.read_csv("data/daao_kmn_related_persons.csv")

def fetch_daao_kmn_related_people_withcount():
    return pd.read_csv("data/daao_kmn_related_people_withcount.csv")

def fetch_daao_recognised_individuals():
    return pd.read_csv("data/daao_recognised_individuals.csv")

def fetch_archibald_participant_data(filter=None):
    warnings.filterwarnings("ignore")
    if filter == "kmn":
        kmn_names = fetch_kmn_names_in_archibald()
        participants_frame = fetch_archibald_participant_data()
        found_participants = pd.DataFrame()
        for kmn_name in kmn_names:
            # change order of words in name
            kmn_name_reordered = " ".join(kmn_name.split(" ")[::-1])
            frame_kmn_name = participants_frame[
                participants_frame["1"].str.contains(kmn_name_reordered)]
            if frame_kmn_name.shape[0] > 0:
                frame_kmn_name["found"] = kmn_name_reordered
            else:
                frame_kmn_name = participants_frame[
                    participants_frame["1"].str.contains(kmn_name)]
                frame_kmn_name["found"] = kmn_name
            found_participants = pd.concat([found_participants, frame_kmn_name])
        return found_participants
    return pd.read_csv('data/archies_allparticipants_byyear.csv')

def fetch_kmn_names_in_archibald():
    with open('data/kmn_names_in_archibald.txt', 'r') as file:
        archie_names = file.read()

    archie_names = archie_names.split("\n")
    return [x.replace("- ", "") for x in archie_names if x.strip() != ""]   

def fetch_kmn_names_in_archibald_as_frame():
    archie_names = fetch_kmn_names_in_archibald()
    kmn_data = fetch_kmn_data()
    kmn_names_in_archibald = kmn_data[
        kmn_data.iloc[:, 0].str.replace(",","").isin(archie_names)]
    
    kmn_names_in_archibald['Artist2'] = kmn_names_in_archibald['Artist'].str.split(", ").apply(lambda x: " ".join(x[::-1]))

    # change Ada Whiting to Ada Clara Whiting
    kmn_names_in_archibald.loc[kmn_names_in_archibald['Artist2'] == 'Ada Whiting', 'Artist2'] = "Ada Clara Whiting"
    return kmn_names_in_archibald

def fetch_plot_data_for_archie_timeline():
    data_found = fetch_kmn_names_in_archibald_as_frame()

    artist_df = pd.DataFrame()
    found_participants = fetch_archibald_participant_data(filter="kmn")
    winners = found_participants[
        found_participants['3'].str.contains('Winner', na=False)]
    artist_names = data_found['Artist2'].unique()

    for artist in artist_names:
        artist_dict = dict()
        w_df = winners[winners["1"] == artist]
        p_df = found_participants[found_participants['found'] == artist]
        this_data_found = data_found[data_found['Artist2'] == artist]
        dob = int(this_data_found['Year of Birth'].values[0])
        try:
            dod = int(this_data_found['Year of Death'].values[0])
        except:
            dod = 2024
        artist_dict[0] = 0 #dob
        
        # generate indicators for each year
        for yr in range(int(dob)+1,int(dod)):
            if len(w_df[w_df['Year'] == yr]): artist_dict[yr-dob] = 3
            elif len(p_df[p_df['Year'] == yr]): artist_dict[yr-dob] = 2
            else: artist_dict[yr-dob] = 1
        
        if (artist_dict[yr-dob] == 1) & (dod != 2024): artist_dict[dod-dob] = 0 #dod
        artist_dict_df = pd.DataFrame(artist_dict.values(), columns=[artist]).T
        artist_df = pd.concat([artist_df, artist_dict_df])

    artist_df = artist_df.fillna(0)
    # sort by first year of participation
    artist_df['First Year'] = artist_df.apply(lambda x: x[x == 2].index[0] if 2 in x.values else None, axis=1)
    artist_df = artist_df.sort_values(by='First Year', ascending=True).drop(columns='First Year')
    return pd.concat([artist_df, pd.DataFrame(columns=range(artist_df.columns[-1]+1, 102))], axis=1)

def fetch_daao_austlist_works():
    return pd.read_csv('data/daao_austlit_works.csv')

@st.dialog("Raw data", width="large")
def inspect_data(frame):
        st.write("")
        st.dataframe(frame)
        
def center_figure(plot_func, *args, **kwargs):
    _, col2, _ = st.columns([1, 5, 1])
    with col2:
        plot_func(*args, **kwargs)