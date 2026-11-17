from dataclasses import dataclass


@dataclass
class Facility:
    facility_id: int
    name: str
    location: str
    capacity: int
    room: str
    facility_type: str
    available: bool = True
    description: str = ""

    def can_accommodate(self, expected_attendance: int) -> bool:
        return self.available and expected_attendance <= self.capacity

    def display_info(self) -> str:
        return (
            f"Facility ID: {self.facility_id}\n"
            f"Name: {self.name}\n"
            f"Location: {self.location}\n"
            f"Room: {self.room}\n"
            f"Type: {self.facility_type}\n"
            f"Capacity: {self.capacity}\n"
            f"Available: {'Yes' if self.available else 'No'}\n"
            f"Description: {self.description}"
        )
