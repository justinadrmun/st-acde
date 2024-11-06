import streamlit as st
from streamlit_option_menu import option_menu
import os
from dotenv import load_dotenv
import page_1
import page_2
import page_3
import page_4
import page_5

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(page_title="Data Visualization App", layout="wide")

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
    # Sidebar for navigation
    selected = option_menu(
        "Main Menu",
        ["Overview", "Trends and Changes", "Comparisons", "Relationships", "Summary and Insights"],
        icons=["house", "chart-line", "bar-chart", "scatter", "info-circle"],
        menu_icon="cast",
        default_index=0,
    )

    # Render selected page
    if selected == "Overview":
        page_1.show()
    elif selected == "Trends and Changes":
        page_2.show()
    elif selected == "Comparisons":
        page_3.show()
    elif selected == "Relationships":
        page_4.show()
    elif selected == "Summary and Insights":
        page_5.show()
