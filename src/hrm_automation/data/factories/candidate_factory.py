"""
Recruitment Candidate Test Data Factory.
Generates unique, collision-resistant candidate records.
"""

import os
import time
import uuid

from faker import Faker

from hrm_automation.data.models.candidate import CandidateData

fake = Faker()


class CandidateFactory:
    """Factory generating isolated synthetic Candidate data records."""

    @classmethod
    def create(
        cls,
        worker_id: str = None,
        **overrides,
    ) -> CandidateData:
        """Generate unique candidate with namespaced email."""
        worker = worker_id or os.getenv("PYTEST_XDIST_WORKER", "m")
        unique_token = uuid.uuid4().hex[:4]
        timestamp = int(time.time()) % 10000

        first_name = f"Cand_{worker}_{unique_token}"
        last_name = f"Talent_{timestamp}"
        email = f"cand_{worker}_{unique_token}_{timestamp}@example-qa.com"
        phone = f"+1555{timestamp:04d}"

        data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "contact_number": phone,
            "keywords": "Automation, Python, Selenium, Quality",
            "notes": "Verified candidate profile.",
        }
        data.update(overrides)

        return CandidateData(**data)
