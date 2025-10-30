from typing import List, Optional
from pydantic import BaseModel, Field


class IsResume(BaseModel):
    """Schema to determine if a document is a resume."""
    is_resume: bool = Field(description="True if the document is a resume or CV, False otherwise.")
    reason: str = Field(description="A brief explanation of why the document is or is not a resume.")



class ResumeProfile(BaseModel):
    """The structured profile extracted from a resume."""
    name: Optional[str] = Field(default=None, description="The full name of the person.")
    email: Optional[str] = Field(default=None, description="The email address of the person.")
    summary: Optional[str] = Field(default=None, description="A 3-sentence summary of the person's profile.")
    top_skills: Optional[List[str]] = Field(default=None, description="An array of the top 3-5 fields of expertise.")
    phd_title: Optional[str] = Field(default=None, description="PhD title, if available.")
    phd_from_college: Optional[str] = Field(default=None, description="The university where the PhD was obtained, if available.")
    latest_three_projects_and_publications: Optional[List[str]] = Field(default=None, description="A list of up to 3 recent projects or publications.")