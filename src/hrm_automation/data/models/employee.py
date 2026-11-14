"""
Data Models for Personnel Information Management (PIM) Domain.
Type-safe Pydantic models for Employee records.
"""

from pydantic import BaseModel


class EmployeeData(BaseModel):
    """Represents synthetic employee test data."""

    first_name: str
    middle_name: str | None = None
    last_name: str
    employee_id: str | None = None
    other_id: str | None = None
    nickname: str | None = None
    driver_license_number: str | None = None
    license_expiry_date: str | None = None
    ssn_number: str | None = None
    sin_number: str | None = None
    nationality: str | None = "American"
    marital_status: str | None = "Single"
    date_of_birth: str | None = "1990-05-15"
    gender: str | None = "Male"

    # Associated login credentials if 'Create Login Details' is checked
    username: str | None = None
    password: str | None = None
    status: str = "Enabled"

    @property
    def full_name(self) -> str:
        """Return combined full name."""
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"
