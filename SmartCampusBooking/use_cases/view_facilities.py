from datetime import datetime
from typing import List, Optional

from SmartCampusBooking.models.facility import Facility
from SmartCampusBooking.services.facility_manager import FacilityManager


class ViewFacilities:
    """Use case for viewing and narrowing facility options."""

    def __init__(self, facility_manager: FacilityManager):
        self.facility_manager = facility_manager

    def display_all_facilities(self) -> List[Facility]:
        facilities = self.facility_manager.get_all_facilities()
        if not facilities:
            print("No facilities available.")
            return []
        for facility in facilities:
            print("-" * 40)
            print(facility.display_info())
        return facilities

    def search_facilities(
        self,
        facility_id: Optional[int] = None,
        location: Optional[str] = None,
        facility_type: Optional[str] = None,
        min_capacity: Optional[int] = None,
    ) -> List[Facility]:
        matches = self.facility_manager.search_facilities(
            facility_id=facility_id,
            location=location,
            facility_type=facility_type,
            min_capacity=min_capacity,
        )
        if not matches:
            print("No facilities matched the provided filters.")
            return []
        for facility in matches:
            print("-" * 40)
            print(facility.display_info())
        return matches

    def get_available_for_datetime(self, event_date: str, start_time: str, end_time: str, reservations=None) -> List[Facility]:
        try:
            parsed_date = datetime.strptime(event_date, "%Y-%m-%d").date()
            start = datetime.strptime(start_time, "%H:%M").time()
            end = datetime.strptime(end_time, "%H:%M").time()
        except ValueError as exc:
            raise ValueError("Please enter valid date and time values in the required format.") from exc

        available = self.facility_manager.get_available_facilities_for_datetime(parsed_date, start, end, reservations)
        if not available:
            print("No facilities are available during the requested period.")
            return []

        for facility in available:
            print("-" * 40)
            print(facility.display_info())
        return available

    def run(self) -> None:
        print("\nFacility Search Options:")
        print("1. View all facilities")
        print("2. Search by ID")
        print("3. Search by location")
        print("4. Search by type")
        print("5. Filter by minimum capacity")
        print("6. Check availability for a day and time")
        print("7. Back")

        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                self.display_all_facilities()
            elif choice == "2":
                facility_id = int(input("Enter facility ID: "))
                self.search_facilities(facility_id=facility_id)
            elif choice == "3":
                location = input("Enter facility location: ").strip()
                self.search_facilities(location=location)
            elif choice == "4":
                facility_type = input("Enter facility type: ").strip()
                self.search_facilities(facility_type=facility_type)
            elif choice == "5":
                capacity = int(input("Enter minimum capacity: "))
                self.search_facilities(min_capacity=capacity)
            elif choice == "6":
                event_date = input("Enter event date (YYYY-MM-DD): ").strip()
                start_time = input("Enter start time (HH:MM): ").strip()
                end_time = input("Enter end time (HH:MM): ").strip()
                self.get_available_for_datetime(event_date, start_time, end_time)
            elif choice == "7":
                return
            else:
                print("Invalid option.")
        except ValueError as exc:
            print(f"Input error: {exc}")
