
import streamlit as st
from .state import GraphState
from .chains import structured_resume_check_llm, structured_profile_extraction_llm
from services.database import check_if_profile_exists, insert_profile

def parse_document(state: GraphState) -> GraphState:
    st.session_state.status_messages.append("Parsing document...")
    return state

def check_if_resume(state: GraphState) -> GraphState:
    st.session_state.status_messages.append("Verifying if document is a resume...")
    prompt = f"Analyze the text to determine if it is a resume or CV.\n\nText:\n---\n{state['file_content'][:2000]}"
    response = structured_resume_check_llm.invoke(prompt)
    state['is_resume'] = response.is_resume
    if not response.is_resume:
        state['final_message'] = f"Document is not a resume. Reason: {response.reason}"
    return state

def extract_profile_info(state: GraphState) -> GraphState:
    """Extracts structured information, leveraging a special section of detected hyperlinks."""
    st.session_state.status_messages.append("Extracting detailed profile information...")
    
    # UPDATED: This prompt now tells the LLM to look for the special hyperlink section.
    prompt = f"""
    Analyze the resume text provided below to extract a comprehensive, structured profile.
    The text may contain a special section at the end called '--- DETECTED HYPERLINKS ---'.
    Use the URLs from that section to accurately fill in the linkedin_url, github_url, and portfolio_url fields.
    If a specific field is not mentioned anywhere, leave its value as null.

    **Extraction Requirements:**
    - `name`, `email`, `phone_number`: Standard contact details.
    - `summary`: A concise professional summary.
    - `top_skills`: A list of the 5 most prominent skills.
    
    - **URL Fields:**
      - `linkedin_url`: Find the LinkedIn URL. Prioritize the list in the 'DETECTED HYPERLINKS' section.
      - `github_url`: Find the GitHub URL. Prioritize the list in the 'DETECTED HYPERLINKS' section.
      - `portfolio_url`: Find the personal portfolio URL. Prioritize the list in the 'DETECTED HYPERLINKS' section.

    - `education`: A detailed list of educational background.
    - `work_experience`: A detailed list of work history.
    - `latest_three_projects_and_publications`: A list of up to 3 projects or publications.

    **Resume Text (including any detected links at the end):**
    ---
    {state['file_content']}
    ---
    """
    response = structured_profile_extraction_llm.invoke(prompt)
    state['profile_data'] = response.dict()
    return state

def check_database(state: GraphState) -> GraphState:
    st.session_state.status_messages.append("Checking database for existing profile...")
    email = state['profile_data'].get('email')
    if email:
        result = check_if_profile_exists.invoke({"email": email})
        state['profile_exists_in_db'] = result['exists']
        if result['exists']:
            state['existing_profile_data'] = result['profile']
            state['final_message'] = "Profile with this email already exists."
    else:
        state['profile_exists_in_db'] = False
        state['final_message'] = "No email found in resume. Inserting new profile."
    return state

def add_to_database(state: GraphState) -> GraphState:
    st.session_state.status_messages.append("Adding new profile to database...")
    insert_profile(state['profile_data'])
    state['final_message'] = "Successfully extracted and added new profile to the database!"
    return state