from dataclasses import dataclass, field
from typing import Optional

from .enums import ReservationStatus
from .event import Event
from .facility import Facility


@dataclass
class Reservation:
    reservation_id: int
    event: Event
    facility: Facility
    status: ReservationStatus = ReservationStatus.PENDING
    approver_id: Optional[int] = None
    rejection_reason: Optional[str] = None

    def approve(self, approver_id: int) -> None:
        if self.status != ReservationStatus.PENDING:
            raise ValueError("Only pending reservations can be approved.")
        self.status = ReservationStatus.APPROVED
        self.approver_id = approver_id
        self.rejection_reason = None

    def reject(self, approver_id: int, rejection_reason: str) -> None:
        if self.status != ReservationStatus.PENDING:
            raise ValueError("Only pending reservations can be rejected.")
        if not rejection_reason.strip():
            raise ValueError("A rejection reason is required.")
        self.status = ReservationStatus.REJECTED
        self.approver_id = approver_id
        self.rejection_reason = rejection_reason.strip()

    def cancel(self, cancelled_by_id: Optional[int] = None) -> None:
        if self.status in (ReservationStatus.REJECTED, ReservationStatus.CANCELLED):
            raise ValueError("Rejected or cancelled reservations cannot be cancelled again.")
        self.status = ReservationStatus.CANCELLED
        self.approver_id = cancelled_by_id if cancelled_by_id is not None else self.approver_id

    def check_status(self) -> ReservationStatus:
        return self.status

    def display_info(self) -> str:
        return (
            f"Reservation ID: {self.reservation_id}\n"
            f"Status: {self.status.value}\n"
            f"Facility: {self.facility.name} ({self.facility.location})\n"
            f"Event: {self.event.event_name}\n"
            f"Requested By: User {self.event.requester_id}\n"
            f"Date: {self.event.event_date.isoformat()}\n"
            f"Time: {self.event.start_time.strftime('%H:%M')} - {self.event.end_time.strftime('%H:%M')}\n"
            f"Expected Attendance: {self.event.expected_attendance}\n"
            f"Special Equipment: {self.event.special_equipment}\n"
            f"Approver ID: {self.approver_id if self.approver_id is not None else 'N/A'}\n"
            f"Rejection Reason: {self.rejection_reason if self.rejection_reason else 'N/A'}"
        )
