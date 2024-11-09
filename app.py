import streamlit as st
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
        st.divider()
        st.write("Some basic visual overviews of the KMN dataset (where each artist in the collection comes from)")

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
