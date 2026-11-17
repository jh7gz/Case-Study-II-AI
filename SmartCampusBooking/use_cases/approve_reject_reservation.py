from SmartCampusBooking.models.enums import UserRole
from SmartCampusBooking.models.user import User
from SmartCampusBooking.services.event_manager import EventManager


class ApproveRejectReservation:
    """Use case for approving or rejecting pending reservations."""

    def __init__(self, event_manager: EventManager):
        self.event_manager = event_manager

    def display_pending(self):
        pending = self.event_manager.get_pending_reservations()
        if not pending:
            print("No pending reservations.")
            return []
        for reservation in pending:
            print("-" * 50)
            print(
                f"Reservation ID: {reservation.reservation_id} | "
                f"Event: {reservation.event.event_name} | "
                f"Facility: {reservation.facility.name}"
            )
        return pending

    def run(self, approver: User) -> None:
        if approver.role not in (UserRole.EVENT_APPROVER, UserRole.FACILITY_COORDINATOR):
            print("Only an Event Approver or Facility Coordinator can approve or reject reservations.")
            return

        pending = self.display_pending()
        if not pending:
            return

        try:
            reservation_id = int(input("Select reservation ID to review: ").strip())
            reservation = self.event_manager.find_reservation_by_id(reservation_id)
            if reservation is None:
                print("Reservation not found.")
                return
            if reservation.status.value != "PENDING":
                print("Only pending reservations can be approved or rejected.")
                return

            print(reservation.display_info())
            action = input("Approve or reject? [approve/reject]: ").strip().lower()
            if action == "approve":
                self.event_manager.approve_reservation(reservation.reservation_id, approver.user_id)
                print("Reservation approved.")
                return
            if action == "reject":
                reason = input("Enter rejection reason: ").strip()
                self.event_manager.reject_reservation(reservation.reservation_id, approver.user_id, reason)
                print("Reservation rejected.")
                return
            print("Invalid action.")
        except ValueError as exc:
            print(f"Approval error: {exc}")
