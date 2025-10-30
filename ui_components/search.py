
import streamlit as st
from services.database import check_if_profile_exists

def render_search():
    st.header("Search Profiles")
    search_email = st.text_input("Enter email to search")
    if st.button("Search by Email"):
        if search_email.strip():
            result = check_if_profile_exists.invoke({"email": search_email})
            if result['exists']:
                st.success("Profile found!")
                st.json(result['profile'])
            else:
                st.warning(f"No profile found with email: {search_email}")
        else:
            st.error("Please enter a valid email.")