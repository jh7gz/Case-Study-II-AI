from typing import List, Optional

from SmartCampusBooking.models.reservation import Reservation
from SmartCampusBooking.models.user import User
from SmartCampusBooking.services.event_manager import EventManager


class TrackReservation:
    """Use case for tracking records by requester or reservation ID."""

    def __init__(self, event_manager: EventManager):
        self.event_manager = event_manager

    def find_by_reservation_id(self, reservation_id: int) -> Optional[Reservation]:
        reservation = self.event_manager.find_reservation_by_id(reservation_id)
        if reservation is None:
            print("No reservation found with that ID.")
            return None
        self.display_reservation(reservation)
        return reservation

    def find_by_requester(self, requester: User) -> List[Reservation]:
        reservations = self.event_manager.find_reservations_by_requester(requester.user_id)
        if not reservations:
            print(f"No reservations found for user {requester.user_id}.")
            return []
        for reservation in reservations:
            self.display_reservation(reservation)
        return reservations

    def display_reservation(self, reservation: Reservation) -> None:
        print("-" * 50)
        print(reservation.display_info())
        print("-" * 50)

    def run(self, requester: User) -> Optional[Reservation]:
        print("\nTrack Reservation Status")
        print("1. Search by reservation ID")
        print("2. View all my reservations")
        print("3. Back")

        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                reservation_id = int(input("Enter reservation ID: ").strip())
                return self.find_by_reservation_id(reservation_id)
            if choice == "2":
                self.find_by_requester(requester)
                return None
            if choice == "3":
                return None
            print("Invalid option.")
            return None
        except ValueError as exc:
            print(f"Input error: {exc}")
            return None
