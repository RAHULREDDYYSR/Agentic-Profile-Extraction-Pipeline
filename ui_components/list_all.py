
import streamlit as st
from services.database import get_all_professors

def render_list_all():
    """Renders the component that lists all professor profiles."""
    st.header("All Professor Profiles")
    
    professors = get_all_professors()
    
    if professors:
        st.success(f"Retrieved {len(professors)} profiles from the database.")
        st.table(professors)
    else:
        st.info("No professors found in the database.")