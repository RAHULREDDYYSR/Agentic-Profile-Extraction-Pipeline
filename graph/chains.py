# graph/chains.py
from langchain_groq import ChatGroq
from .schemas import IsResume, ResumeProfile

# Using Llama3 8B for speed, can be switched to 70B for higher accuracy
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# Create structured LLMs for specific tasks
structured_resume_check_llm = llm.with_structured_output(IsResume)
structured_profile_extraction_llm = llm.with_structured_output(ResumeProfile)