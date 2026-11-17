from dataclasses import dataclass
from datetime import date, time


@dataclass
class Event:
    event_id: int
    requester_id: int
    organization: str
    event_name: str
    event_date: date
    start_time: time
    end_time: time
    expected_attendance: int
    special_equipment: str
    description: str

    def is_valid(self) -> bool:
        if self.expected_attendance <= 0:
            return False
        if self.end_time <= self.start_time:
            return False
        return True

    def display_info(self) -> str:
        return (
            f"Event ID: {self.event_id}\n"
            f"Requester ID: {self.requester_id}\n"
            f"Organization: {self.organization}\n"
            f"Event Name: {self.event_name}\n"
            f"Date: {self.event_date.isoformat()}\n"
            f"Time: {self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}\n"
            f"Expected Attendance: {self.expected_attendance}\n"
            f"Special Equipment: {self.special_equipment}\n"
            f"Description: {self.description}"
        )
