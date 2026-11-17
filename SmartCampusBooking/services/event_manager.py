from datetime import date, time
from typing import List, Optional

from SmartCampusBooking.models.enums import ReservationStatus, UserRole
from SmartCampusBooking.models.event import Event
from SmartCampusBooking.models.facility import Facility
from SmartCampusBooking.models.reservation import Reservation


class EventManager:
    """Central service for creating, tracking, and changing reservations."""

    def __init__(self):
        self.events: List[Event] = []
        self.reservations: List[Reservation] = []
        self._next_event_id = 1
        self._next_reservation_id = 1

    def _next_event_number(self) -> int:
        value = self._next_event_id
        self._next_event_id += 1
        return value

    def _next_reservation_number(self) -> int:
        value = self._next_reservation_id
        self._next_reservation_id += 1
        return value

    def create_event(
        self,
        requester_id: int,
        organization: str,
        event_name: str,
        event_date: date,
        start_time: time,
        end_time: time,
        expected_attendance: int,
        special_equipment: str,
        description: str,
    ) -> Event:
        if event_name.strip() == "":
            raise ValueError("Event name is required.")
        if organization.strip() == "":
            raise ValueError("Organization is required.")
        event = Event(
            event_id=self._next_event_number(),
            requester_id=requester_id,
            organization=organization.strip(),
            event_name=event_name.strip(),
            event_date=event_date,
            start_time=start_time,
            end_time=end_time,
            expected_attendance=expected_attendance,
            special_equipment=special_equipment.strip(),
            description=description.strip(),
        )
        if not event.is_valid():
            raise ValueError("Event details are invalid. Ensure a valid date, positive attendance, and end time after start time.")
        self.events.append(event)
        return event

    def create_reservation(self, event: Event, facility: Facility) -> Reservation:
        if not facility.available:
            raise ValueError("The facility is unavailable for reservations.")
        if event.expected_attendance > facility.capacity:
            raise ValueError("Expected attendance exceeds facility capacity.")
        if self.check_for_conflict(facility, event.event_date, event.start_time, event.end_time):
            raise ValueError("The facility is already reserved during that time.")

        reservation = Reservation(
            reservation_id=self._next_reservation_number(),
            event=event,
            facility=facility,
            status=ReservationStatus.PENDING,
        )
        self.reservations.append(reservation)
        return reservation

    def find_reservation_by_id(self, reservation_id: int) -> Optional[Reservation]:
        for reservation in self.reservations:
            if reservation.reservation_id == reservation_id:
                return reservation
        return None

    def find_reservations_by_requester(self, requester_id: int) -> List[Reservation]:
        return [reservation for reservation in self.reservations if reservation.event.requester_id == requester_id]

    def get_pending_reservations(self) -> List[Reservation]:
        return [reservation for reservation in self.reservations if reservation.status == ReservationStatus.PENDING]

    def check_for_conflict(
        self,
        facility: Facility,
        event_date,
        start_time: time,
        end_time: time,
        exclude_reservation_id: Optional[int] = None,
        include_pending: bool = False,
    ) -> bool:
        if end_time <= start_time:
            return True

        for reservation in self.reservations:
            if exclude_reservation_id is not None and reservation.reservation_id == exclude_reservation_id:
                continue
            if reservation.facility.facility_id != facility.facility_id:
                continue
            if reservation.status == ReservationStatus.REJECTED or reservation.status == ReservationStatus.CANCELLED:
                continue
            if reservation.status != ReservationStatus.APPROVED and not include_pending:
                continue
            if reservation.status == ReservationStatus.PENDING and not include_pending:
                continue
            if reservation.event.event_date != event_date:
                continue
            if start_time < reservation.event.end_time and end_time > reservation.event.start_time:
                return True
        return False

    def approve_reservation(self, reservation_id: int, approver_id: int) -> Reservation:
        reservation = self.find_reservation_by_id(reservation_id)
        if reservation is None:
            raise ValueError("Reservation not found.")
        if reservation.status != ReservationStatus.PENDING:
            raise ValueError("Only pending reservations can be approved.")
        if reservation.facility.available is False:
            raise ValueError("The facility is not available for approval.")
        if self.check_for_conflict(
            reservation.facility,
            reservation.event.event_date,
            reservation.event.start_time,
            reservation.event.end_time,
            exclude_reservation_id=reservation_id,
            include_pending=True,
        ):
            raise ValueError("This reservation overlaps with another approved or pending reservation.")

        reservation.approve(approver_id)
        return reservation

    def reject_reservation(self, reservation_id: int, approver_id: int, rejection_reason: str) -> Reservation:
        reservation = self.find_reservation_by_id(reservation_id)
        if reservation is None:
            raise ValueError("Reservation not found.")
        if reservation.status != ReservationStatus.PENDING:
            raise ValueError("Only pending reservations can be rejected.")
        reservation.reject(approver_id, rejection_reason)
        return reservation

    def cancel_reservation(
        self,
        reservation_id: int,
        actor_id: int,
        actor_role: Optional[UserRole] = None,
    ) -> Reservation:
        reservation = self.find_reservation_by_id(reservation_id)
        if reservation is None:
            raise ValueError("Reservation not found.")
        if reservation.status in (ReservationStatus.REJECTED, ReservationStatus.CANCELLED):
            raise ValueError("Rejected or already cancelled reservations cannot be cancelled again.")

        if actor_role in (UserRole.SYSTEM_ADMINISTRATOR, UserRole.FACILITY_COORDINATOR):
            reservation.cancel(actor_id)
            return reservation

        if reservation.event.requester_id != actor_id:
            raise ValueError("Only the requester or an authorized administrator can cancel this reservation.")

        reservation.cancel(actor_id)
        return reservation
