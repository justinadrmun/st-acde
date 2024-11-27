import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from utils import fetch_kmn_data, inspect_data
from dotenv import load_dotenv
import os

# Set page configuration
st.set_page_config(page_title="Data Visualization App", layout="wide")

# Load environment variables
load_dotenv()

# Password-protected access
def check_password():
    def password_entered():
        if st.session_state["password"] == os.getenv('APP_PASSWORD'):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # remove password from session
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input(
            "Enter Password",
            type="password",
            on_change=password_entered,
            key="password",
        )
        return False
    elif not st.session_state["password_correct"]:
        st.text_input(
            "Enter Password",
            type="password",
            on_change=password_entered,
            key="password",
        )
        st.error("😕 Incorrect password")
        return False
    else:
        return True

if check_password():
    st.title("Know My Name")
    options = ["Overview", "Exhibition", "Subjects", "Society", "Space", "Time"]
    selection = st.segmented_control(
        "placeholder", options, selection_mode="single", default="Overview", label_visibility="hidden"
    )
    if selection == "Overview":
        st.header("Overview")
        with st.expander("About the Dataset", expanded=False):
            st.markdown("""
                        #### Basic Information
                        - The dataset contains **283 entries** and **31 columns**.
                        - The columns include various attributes related to artists and their exhibitions.

                        #### Descriptive Statistics
                        - **Artist Name and Link to Know My Name Exhibition Page**: 283 unique entries.
                        - **Collective/Individual**: Mostly "Individual" (263 out of 282 entries).
                        - **First Nations People Group (from Know My Name only)**: 40 entries, with "Gija People" being the most frequent (3 times).
                        - **Place of Birth (First Nations Language)**: 230 entries, with "Gadigal Land" being the most frequent (53 times).
                        - **Place of Birth (Anglophone)**: 269 entries, with "Sydney" being the most frequent (46 times).
                        - **State of Birth**: 248 entries, with "NSW" being the most frequent (67 times).
                        - **Country of Birth**: 275 entries, with "Australia" being the most frequent (226 times).
                        - **Place of Birth Latitude and Longitude**: 274 entries each, with mean latitude of -20.64 and mean longitude of 120.40.
                        - **Year of Birth**: 282 entries, with 1959 being the most frequent year (10 times).
                        - **Date of Birth**: 126 entries.
                        - **Place of Death (Indigenous)**: 252 entries.
                        - **Place of Death (Anglophone)**: 267 entries.
                        - **State of Death**: 265 entries.
                        - **Country of Death**: 269 entries.
                        - **Place of Death Latitude and Longitude**: 97 entries each.
                        - **Year of Death**: 283 entries.
                        - **Date of Death**: 261 entries.
                        - **Link to DAAO**: 279 entries.
                        - **In DAAO 2,188**: 282 entries.
                        - **Link to AWR**: 22 entries.
                        - **Author of NGA Essay**: 155 entries, with "Tina Baum" being the most frequent (6 times).
                        - **Page of Book**: 155 entries, with a mean of 205.69 pages.
                        - **Anne Marsh Critic Author Full Citations**: 34 entries.
                        - **Anne Marsh Critic Authors**: 33 entries.
                        - **Anne Marsh Discussions**: 68 entries.
                        - **Illustration Included?**: 68 entries, with "Y" being the most frequent (62 times).
                        - **Link to NLA**: 281 entries.
                        - **Multiple NLA**: 281 entries.
                        - **Missing NLA**: 281 entries.

                        #### Missing Values
                        - Significant missing values in columns like "First Nations People Group (from Know My Name only)" (243 missing), "Date of Birth" (157 missing), "Place of Death Latitude" (186 missing), and "Link to AWR" (261 missing).
            """
            )
        kmn = fetch_kmn_data()
        if st.button("Inspect data :mag_right:"):
                inspect_data(kmn)
        
        st.divider()
        col1, col2, col3 = st.columns([0.5, 0.3, 0.2], gap="large")
        with col1:
            st.caption("Year of Birth of KMN Artists, by Decade.") 

            # show missing values for year of birth
            kmn_dob = kmn[kmn['Year of Birth'].notnull()]

            # most values are integers, but some are strings i.e., '1887 or 1885'
            kmn_dob['Year of Birth'] = kmn_dob['Year of Birth'].str.extract(r'(\d{4})').astype(int)

            fig, ax = plt.subplots(figsize=(16, 6))
            # bar plot of year of birth in decade buckets
            bins = np.arange(1820, 2030, 10)
            n, bins, patches = ax.hist(kmn_dob['Year of Birth'], bins=bins, edgecolor='white')

            # Add labels to the bars
            for patch in patches:
                height = patch.get_height()
                ax.text(patch.get_x() + patch.get_width() / 2, height + 1, int(height), ha='center', va='bottom')
            
            # Set x-axis ticks to show every 20 years
            ax.set_xticks(np.arange(1820, 2040, 20))
            ax.set_ylim(0, max(n) + 5)

            ax.set_title("")
            ax.set_xlabel("Year of Birth")
            ax.set_ylabel("Number of Artists")

            st.pyplot(fig)
            st.caption("*Note that this excludes artists with missing values for year of birth i.e., Ken Family Collaborative.*") 

        with col2:
            st.caption("Year of Birth, Oldest and Youngest.")
            oldest_year = kmn_dob['Year of Birth'].min()
            youngest_year = kmn_dob['Year of Birth'].max()
            old_val = kmn_dob[kmn_dob['Year of Birth'] == oldest_year]['Artist'].values[0]
            young_val = kmn_dob[kmn_dob['Year of Birth'] == youngest_year]['Artist'].values[0]
            st.metric(value=old_val, label=str(oldest_year))
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.metric(value=young_val, label=str(youngest_year))
            
        with col3:
            st.caption("Proportion of artists still living.")
            kmn["Alive"] = kmn['Year of Death'] == 'N/A (Still Living)'
            
            fig, ax = plt.subplots()
            kmn["Alive"].value_counts().plot.pie(autopct='%1.1f%%', ax=ax, labels=['Alive', 'Deceased'])
            ax.set_ylabel("")
            ax.set_xlabel("")
            st.pyplot(fig)

        st.divider()
        st.caption("Some basic visual overviews of the KMN dataset (where each artist in the collection comes from)")
        col1, col2, col3 = st.columns([1, 1, 3])

        with col2:
            # plot a horizontal bar chart of the number of artists from each country
            st.write("No. of artists from each country")
            st.bar_chart(kmn["Country of Birth"].value_counts(), horizontal=True)
        
        with col1:
            # plot a horizontal bar chart of the number of artists from each state
            st.write("No. of artists from each state")
            st.bar_chart(kmn["State of Birth"].value_counts(), horizontal=True)

        with col3:
            # plot a map of the artists' birthplaces
            st.write("Map of artists' birthplaces")
            st.map(kmn[["Place of Birth Latitude", "Place of Birth Longitude"]]
                    .dropna()
                    .rename(
                    columns={"Place of Birth Latitude": "lat", 
                                "Place of Birth Longitude": "lon"}))

    if selection == "Exhibition":
        import page_1
        page_1.show()

    if selection == "Subjects":
        import page_2
        page_2.show()

    if selection == "Society":
        import page_3
        page_3.show()

    if selection == "Space":
        import page_4
        page_4.show()

    if selection == "Time":
        import page_5
        page_5.show()
