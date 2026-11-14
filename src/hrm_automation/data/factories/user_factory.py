"""
System User Test Data Factory.
Generates unique usernames and compliant passwords with worker isolation.
"""

import os
import time
import uuid

from faker import Faker

from hrm_automation.data.models.user import SystemUserData

fake = Faker()


class UserFactory:
    """Factory generating collision-resistant system user data."""

    @classmethod
    def create(
        cls,
        employee_name: str,
        user_role: str = "ESS",
        status: str = "Enabled",
        worker_id: str = None,
        **overrides,
    ) -> SystemUserData:
        """
        Generate a unique SystemUserData instance.
        Username format: usr_{worker}_{token}_{ts} (must be between 5 and 40 characters)
        Password requires: >= 8 chars, 1 uppercase, 1 lowercase, 1 number, 1 symbol
        """
        worker = worker_id or os.getenv("PYTEST_XDIST_WORKER", "m")
        unique_token = uuid.uuid4().hex[:4]
        timestamp = int(time.time()) % 10000

        username = f"usr_{worker}_{unique_token}_{timestamp}"
        password = f"P@ssw0rd_{unique_token}!"

        data = {
            "user_role": user_role,
            "employee_name": employee_name,
            "status": status,
            "username": username,
            "password": password,
            "confirm_password": password,
        }
        data.update(overrides)

        return SystemUserData(**data)
