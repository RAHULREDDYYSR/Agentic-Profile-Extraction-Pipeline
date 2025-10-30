# graph/graph.py
from typing import Literal
from langgraph.graph import StateGraph, END
from .state import GraphState
from .nodes import (
    parse_document, check_if_resume, extract_profile_info,
    check_database, add_to_database
)

def decide_what_to_do_after_resume_check(state: GraphState) -> Literal["extract_profile", "end_not_resume"]:
    return "extract_profile" if state['is_resume'] else "end_not_resume"

def decide_after_db_check(state: GraphState) -> Literal["add_to_db", "end_exists"]:
    return "end_exists" if state['profile_exists_in_db'] else "add_to_db"

# Define the workflow graph
workflow = StateGraph(GraphState)
workflow.add_node("parse_document", parse_document)
workflow.add_node("check_if_resume", check_if_resume)
workflow.add_node("extract_profile_info", extract_profile_info)
workflow.add_node("check_database", check_database)
workflow.add_node("add_to_database", add_to_database)

# Build the graph
workflow.set_entry_point("parse_document")
workflow.add_edge("parse_document", "check_if_resume")
workflow.add_conditional_edges("check_if_resume", decide_what_to_do_after_resume_check, 
                               {"extract_profile": "extract_profile_info", "end_not_resume": END})
workflow.add_edge("extract_profile_info", "check_database")
workflow.add_conditional_edges("check_database", decide_after_db_check, 
                               {"add_to_db": "add_to_database", "end_exists": END})
workflow.add_edge("add_to_database", END)

# Compile the graph
app = workflow.compile()

app.get_graph().draw_mermaid_png(output_file_path="graph.png")