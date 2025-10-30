# graph/state.py
from typing import Optional

class GraphState(dict):
    """Defines the state for our LangGraph workflow."""
    file_content: str
    is_resume: bool
    profile_data: dict
    profile_exists_in_db: bool
    existing_profile_data: Optional[dict]
    final_message: str