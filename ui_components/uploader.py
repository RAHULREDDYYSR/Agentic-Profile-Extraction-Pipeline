
import streamlit as st
from services.file_parser import get_file_text
from graph.state import GraphState

def render_uploader(graph_app):
    """Renders the uploader and processes the file using a clean status UI."""
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt"])

    if uploaded_file:
        st.session_state.status_messages = []
        final_state = None  # Initialize to ensure variable is available outside the with block

        # Use st.status to show the process steps. This container will be collapsed.
        with st.status("Processing resume...", expanded=True) as status:
            try:
                file_text = get_file_text(uploaded_file)
                
                if not file_text.strip():
                    status.update(label="Failed to extract text from file.", state="error", expanded=False)
                    return

                # Run the graph and get the final state
                initial_state = GraphState(file_content=file_text)
                final_state = graph_app.invoke(initial_state)

                # Display the completed steps inside the status box before it collapses
                for msg in st.session_state.status_messages:
                    st.write(f"✔️ {msg}")

                # Determine the final state of the status box
                final_label = final_state.get('final_message', "Processing complete.")
                final_status_state = "complete"
                
                if final_state.get('is_resume') == False or final_state.get('profile_exists_in_db'):
                    final_status_state = "error"
                
                # Update and collapse the status box
                status.update(label=final_label, state=final_status_state, expanded=False)

            except Exception as e:
                status.update(label=f"An unexpected error occurred: {e}", state="error", expanded=False)

        # --- Display the Final Result (OUTSIDE the status block) ---
        # This code runs after the 'with' block has finished and the status box is collapsed.
        # It ensures the final JSON data is always visible.
        if final_state:
            if final_state.get('is_resume') == False:
                # The warning is already shown in the collapsed status box, so we don't need to do anything here.
                pass
            elif final_state.get('profile_exists_in_db'):
                st.info("Displaying existing profile from the database:")
                st.json(final_state['existing_profile_data'])
            elif final_state.get('profile_data'):
                st.success("Extracted Profile Data:")
                st.json(final_state['profile_data'])