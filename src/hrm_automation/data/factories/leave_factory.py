"""
Leave Test Data Factory.
Generates dynamic leave applications with compliant date ranges and comments.
"""

from datetime import datetime, timedelta

from faker import Faker

from hrm_automation.data.models.leave import LeaveApplicationData

fake = Faker()


class LeaveFactory:
    """Factory generating valid LeaveApplicationData instances."""

    @classmethod
    def create(
        cls,
        days_in_future: int = 14,
        duration_days: int = 2,
        leave_type: str = "US - Vacation",
        **overrides,
    ) -> LeaveApplicationData:
        """
        Generate dynamic leave dates relative to today.
        Format required by OrangeHRM date picker: YYYY-MM-DD or YYYY-DD-MM (ISO standard YYYY-MM-DD works reliably).
        """
        start = datetime.now() + timedelta(days=days_in_future)
        end = start + timedelta(days=duration_days - 1)

        from_date_str = start.strftime("%Y-%m-%d")
        to_date_str = end.strftime("%Y-%m-%d")

        data = {
            "leave_type": leave_type,
            "from_date": from_date_str,
            "to_date": to_date_str,
            "comment": f"Automated Leave Request - {fake.sentence(nb_words=4)}",
        }
        data.update(overrides)

        return LeaveApplicationData(**data)
