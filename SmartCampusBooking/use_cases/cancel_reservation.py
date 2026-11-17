from typing import Optional

from SmartCampusBooking.models.enums import UserRole
from SmartCampusBooking.models.user import User
from SmartCampusBooking.services.event_manager import EventManager


class CancelReservation:
    """Use case for cancelling a reservation request."""

    def __init__(self, event_manager: EventManager):
        self.event_manager = event_manager

    def run(self, requester: User) -> None:
        try:
            reservation_id = int(input("Enter reservation ID to cancel: ").strip())
            reservation = self.event_manager.find_reservation_by_id(reservation_id)
            if reservation is None:
                print("Reservation not found.")
                return

            if reservation.status.value in ("REJECTED", "CANCELLED"):
                print("This reservation cannot be cancelled because it is already rejected or cancelled.")
                return

            if requester.role in (UserRole.SYSTEM_ADMINISTRATOR, UserRole.FACILITY_COORDINATOR):
                self.event_manager.cancel_reservation(reservation_id, requester.user_id, requester.role)
                print("Reservation cancelled by authorized administrator.")
                return

            if reservation.event.requester_id != requester.user_id:
                print("You are not authorized to cancel this reservation.")
                return

            self.event_manager.cancel_reservation(reservation_id, requester.user_id)
            print("Reservation cancelled successfully.")
        except ValueError as exc:
            print(f"Cancellation error: {exc}")
