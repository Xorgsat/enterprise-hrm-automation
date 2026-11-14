"""
Data Model for Recruitment Domain.
Type-safe Pydantic model for Candidates.
"""

from pydantic import BaseModel


class CandidateData(BaseModel):
    """Represents a job candidate record in Recruitment > Candidates."""

    first_name: str
    middle_name: str | None = None
    last_name: str
    email: str
    contact_number: str | None = None
    keywords: str | None = "QA, SDET, Automation, Python, Selenium"
    notes: str | None = "Candidate automatically generated for pipeline automation"
    status: str = "Application Initiated"

    @property
    def full_name(self) -> str:
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"
