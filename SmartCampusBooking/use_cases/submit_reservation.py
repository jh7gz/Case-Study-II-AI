from datetime import datetime
from typing import Optional

from SmartCampusBooking.models.event import Event
from SmartCampusBooking.models.facility import Facility
from SmartCampusBooking.models.user import User
from SmartCampusBooking.services.event_manager import EventManager
from SmartCampusBooking.services.facility_manager import FacilityManager


class SubmitReservation:
    """Use case for creating a new reservation request."""

    def __init__(self, facility_manager: FacilityManager, event_manager: EventManager):
        self.facility_manager = facility_manager
        self.event_manager = event_manager

    def submit(
        self,
        requester: User,
        facility_id: int,
        organization: str,
        event_name: str,
        event_date: str,
        start_time: str,
        end_time: str,
        expected_attendance: int,
        special_equipment: str,
        description: str,
    ):
        facility = self.facility_manager.find_by_id(facility_id)
        if facility is None:
            raise ValueError("Facility not found.")
        if not facility.available:
            raise ValueError("The selected facility is unavailable for reservations.")

        try:
            parsed_date = datetime.strptime(event_date, "%Y-%m-%d").date()
            start = datetime.strptime(start_time, "%H:%M").time()
            end = datetime.strptime(end_time, "%H:%M").time()
        except ValueError as exc:
            raise ValueError("Invalid date or time format. Use YYYY-MM-DD and HH:MM.") from exc

        if expected_attendance <= 0:
            raise ValueError("Expected attendance must be positive.")
        if expected_attendance > facility.capacity:
            raise ValueError("Expected attendance exceeds facility capacity.")
        if end <= start:
            raise ValueError("End time must be after start time.")
        if self.event_manager.check_for_conflict(facility, parsed_date, start, end):
            raise ValueError("This facility is already reserved during the requested time.")

        event = self.event_manager.create_event(
            requester_id=requester.user_id,
            organization=organization,
            event_name=event_name,
            event_date=parsed_date,
            start_time=start,
            end_time=end,
            expected_attendance=expected_attendance,
            special_equipment=special_equipment,
            description=description,
        )

        reservation = self.event_manager.create_reservation(event, facility)
        print("Reservation submitted successfully.")
        print(reservation.display_info())
        return reservation

    def run(self, requester: User) -> Optional[object]:
        print("\nSubmit Reservation Request")
        print("Available facilities:")
        for facility in self.facility_manager.get_all_facilities():
            print(f"{facility.facility_id}. {facility.name} ({facility.location}) - Capacity {facility.capacity}")

        try:
            facility_id = int(input("Select facility ID: ").strip())
            organization = input("Organization name: ").strip()
            event_name = input("Event name: ").strip()
            event_date = input("Event date (YYYY-MM-DD): ").strip()
            start_time = input("Start time (HH:MM): ").strip()
            end_time = input("End time (HH:MM): ").strip()
            expected_attendance = int(input("Expected attendance: ").strip())
            special_equipment = input("Special equipment requirements: ").strip()
            description = input("Event description: ").strip()

            return self.submit(
                requester=requester,
                facility_id=facility_id,
                organization=organization,
                event_name=event_name,
                event_date=event_date,
                start_time=start_time,
                end_time=end_time,
                expected_attendance=expected_attendance,
                special_equipment=special_equipment,
                description=description,
            )
        except ValueError as exc:
            print(f"Reservation error: {exc}")
            return None
