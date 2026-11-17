from datetime import date, time
from typing import Iterable, List, Optional

from SmartCampusBooking.models.facility import Facility
from SmartCampusBooking.models.reservation import Reservation
from SmartCampusBooking.models.enums import ReservationStatus


class FacilityManager:
    """Manage catalog information for campus facilities."""

    def __init__(self, facilities: Optional[List[Facility]] = None):
        self.facilities: List[Facility] = facilities if facilities is not None else []

    def get_all_facilities(self) -> List[Facility]:
        return self.facilities

    def find_by_id(self, facility_id: int) -> Optional[Facility]:
        for facility in self.facilities:
            if facility.facility_id == facility_id:
                return facility
        return None

    def search_facilities(
        self,
        facility_id: Optional[int] = None,
        location: Optional[str] = None,
        facility_type: Optional[str] = None,
        min_capacity: Optional[int] = None,
    ) -> List[Facility]:
        matches: List[Facility] = []

        for facility in self.facilities:
            if facility_id is not None and facility.facility_id != facility_id:
                continue
            if location is not None and facility.location.lower() != location.lower():
                continue
            if facility_type is not None and facility.facility_type.lower() != facility_type.lower():
                continue
            if min_capacity is not None and facility.capacity < min_capacity:
                continue
            matches.append(facility)
        return matches

    def get_available_facilities_for_datetime(
        self,
        event_date: date,
        start_time: time,
        end_time: time,
        reservations: Optional[Iterable[Reservation]] = None,
    ) -> List[Facility]:
        if reservations is None:
            reservations = []

        available: List[Facility] = []
        for facility in self.facilities:
            if not facility.available:
                continue

            conflict = False
            for reservation in reservations:
                if reservation.facility.facility_id != facility.facility_id:
                    continue
                if reservation.status != ReservationStatus.APPROVED:
                    continue
                if reservation.event.event_date != event_date:
                    continue
                if start_time < reservation.event.end_time and end_time > reservation.event.start_time:
                    conflict = True
                    break

            if not conflict:
                available.append(facility)

        return available
