"""
Data Model for System Users in Admin Domain.
Type-safe Pydantic model for User accounts.
"""

from pydantic import BaseModel


class SystemUserData(BaseModel):
    """Represents a system user account in Admin > User Management."""

    user_role: str = "ESS"  # "Admin" or "ESS"
    employee_name: str
    status: str = "Enabled"  # "Enabled" or "Disabled"
    username: str
    password: str
    confirm_password: str | None = None

    def model_post_init(self, __context) -> None:
        if not self.confirm_password:
            self.confirm_password = self.password
