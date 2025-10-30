
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from ui_components.uploader import render_uploader
from ui_components.search import render_search
from ui_components.list_all import render_list_all
from graph.graph import app as resume_graph_app


# --- Main Streamlit Application ---

st.set_page_config(layout="wide", page_title="AI Resume Screener")

# --- Session State Management ---
# Initialize the active_view state if it doesn't exist.
# This ensures a default view is shown on first load.
if 'active_view' not in st.session_state:
    st.session_state.active_view = "uploader"

# --- Sidebar for Navigation ---
# The sidebar will contain the buttons to toggle between different views.
with st.sidebar:
    st.title("📄 Resume AI")
    st.markdown("---")
    st.header("Navigation")

    # The on_click functions now simply update the session state.
    # use_container_width makes the buttons fill the sidebar width for a cleaner look.
    st.button(
        "Upload & Process Resume",
        on_click=lambda: st.session_state.update(active_view="uploader"),
        use_container_width=True,
        type="primary" if st.session_state.active_view == "uploader" else "secondary"
    )

    st.button(
        "Search Profiles",
        on_click=lambda: st.session_state.update(active_view="search"),
        use_container_width=True,
        type="primary" if st.session_state.active_view == "search" else "secondary"
    )

    st.button(
        "Show All Profiles",
        on_click=lambda: st.session_state.update(active_view="list_all"),
        use_container_width=True,
        type="primary" if st.session_state.active_view == "list_all" else "secondary"
    )
    
    st.markdown("---")
    st.caption("Built with LangGraph & Groq.")


# --- Main Content Area ---
# The main area of the app will render a different component based
# on the value of st.session_state.active_view.

# Initialize session state for status messages used by the uploader graph
if 'status_messages' not in st.session_state:
    st.session_state.status_messages = []

# Conditionally render the selected view
if st.session_state.active_view == "uploader":
    st.title("AI-Powered Resume Analysis")
    st.markdown("Upload a resume (PDF, DOCX, TXT) to automatically extract key information and save it to the database.")
    st.markdown("---")
    render_uploader(resume_graph_app)

elif st.session_state.active_view == "search":
    st.title("Search Existing Profiles")
    st.markdown("Find a specific profile in the database by searching for their email address.")
    st.markdown("---")
    render_search()

elif st.session_state.active_view == "list_all":
    st.title("Browse All Profiles")
    st.markdown("View a list of all the professor profiles currently stored in the database.")
    st.markdown("---")
    render_list_all()