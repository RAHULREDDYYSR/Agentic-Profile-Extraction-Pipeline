# graph/nodes.py
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
    st.session_state.status_messages.append("Extracting profile information...")
    prompt = f"Extract information from the resume text. If a field isn't mentioned, leave it null.\n\nText:\n---\n{state['file_content']}"
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