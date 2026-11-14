"""
Synthetic Employee Test Data Factory.
Generates collision-resistant, valid test data compliant with OrangeHRM form constraints.
"""

import os
import time
import uuid

from faker import Faker

from hrm_automation.data.models.employee import EmployeeData

fake = Faker()


class EmployeeFactory:
    """Factory generating isolated synthetic Employee data records."""

    @classmethod
    def create(
        cls,
        worker_id: str = None,
        include_login_details: bool = False,
        **overrides,
    ) -> EmployeeData:
        """
        Generate a unique EmployeeData instance with collision-resistant namespacing.
        Example format: First: Aut_W0_8a1b, Last: Doe_3914
        """
        worker = worker_id or os.getenv("PYTEST_XDIST_WORKER", "m")
        unique_token = uuid.uuid4().hex[:4]
        timestamp = int(time.time()) % 100000

        # OrangeHRM first/last name max lengths and allowed characters
        first_name = f"Aut_{worker}_{unique_token}"
        middle_name = fake.first_name()[:8]
        last_name = f"Test_{timestamp}"

        # 6-digit numeric employee ID with collision protection
        emp_id = f"{timestamp:05d}{unique_token[:1]}"
        nickname = f"Nick_{unique_token}"
        other_id = f"OID_{unique_token}"
        driver_license = f"DL{timestamp}"

        username = None
        password = None
        if include_login_details:
            username = f"user_{worker}_{unique_token}_{timestamp}"
            password = f"P@ssw0rd_{unique_token}!"

        data = {
            "first_name": first_name,
            "middle_name": middle_name,
            "last_name": last_name,
            "employee_id": emp_id,
            "nickname": nickname,
            "other_id": other_id,
            "driver_license_number": driver_license,
            "username": username,
            "password": password,
        }
        data.update(overrides)

        return EmployeeData(**data)
