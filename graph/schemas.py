
from typing import List, Optional
from pydantic import BaseModel, Field


class IsResume(BaseModel):
    """Schema to determine if a document is a resume."""
    is_resume: bool = Field(description="True if the document is a resume or CV, False otherwise.")
    reason: str = Field(description="A brief explanation of why the document is or is not a resume.")

# NEW: A model to represent a single educational institution
class Education(BaseModel):
    """Represents a single educational entry from a resume."""
    institution: Optional[str] = Field(default=None, description="Name of the university or college.")
    degree: Optional[str] = Field(default=None, description="The degree obtained, e.g., 'Master of Science'.")
    field_of_study: Optional[str] = Field(default=None, description="The field of study, e.g., 'Computer Science'.")
    graduation_date: Optional[str] = Field(default=None, description="The year or full date of graduation.")

# NEW: A model to represent a single job experience
class WorkExperience(BaseModel):
    """Represents a single work experience entry from a resume."""
    company: Optional[str] = Field(default=None, description="Name of the company.")
    job_title: Optional[str] = Field(default=None, description="The job title or position.")
    start_date: Optional[str] = Field(default=None, description="The start date of the employment.")
    end_date: Optional[str] = Field(default=None, description="The end date of the employment (can be 'Present').")
    description: Optional[str] = Field(default=None, description="A brief summary of responsibilities and achievements.")

# UPDATED: The main profile now includes lists for education and work experience
class ResumeProfile(BaseModel):
    """The structured profile extracted from a resume."""
    name: Optional[str] = Field(default=None, description="The full name of the person.")
    email: Optional[str] = Field(default=None, description="The email address of the person.")
    phone_number: Optional[str] = Field(default=None, description="The phone number of the person.")
    linkedin_url: Optional[str] = Field(default=None, description="URL of the person's LinkedIn profile.")
    github_url: Optional[str] = Field(default=None, description="URL of the person's GitHub profile.")
    portfolio_url: Optional[str] = Field(default=None, description="URL of the person's personal website or portfolio.")
    summary: Optional[str] = Field(default=None, description="A 3-sentence summary of the person's professional profile.")
    top_skills: Optional[List[str]] = Field(default=None, description="An array of the top 5 most relevant skills.")
    
    # Nested lists of our new models
    education: Optional[List[Education]] = Field(default=None, description="A list of the person's educational background.")
    work_experience: Optional[List[WorkExperience]] = Field(default=None, description="A list of the person's work experience.")
    