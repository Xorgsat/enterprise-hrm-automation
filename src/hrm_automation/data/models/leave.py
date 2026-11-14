"""
Data Model for Leave Management Domain.
Type-safe Pydantic model for Leave Applications.
"""

from pydantic import BaseModel


class LeaveApplicationData(BaseModel):
    """Represents a leave application request."""

    leave_type: str = "US - Vacation"
    from_date: str
    to_date: str
    comment: str | None = None
    partial_days: str | None = None
    duration: str | None = None
