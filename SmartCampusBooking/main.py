from datetime import date, time

from SmartCampusBooking.models.enums import UserRole
from SmartCampusBooking.models.facility import Facility
from SmartCampusBooking.models.user import User
from SmartCampusBooking.services.event_manager import EventManager
from SmartCampusBooking.services.facility_manager import FacilityManager
from SmartCampusBooking.use_cases.approve_reject_reservation import ApproveRejectReservation
from SmartCampusBooking.use_cases.cancel_reservation import CancelReservation
from SmartCampusBooking.use_cases.submit_reservation import SubmitReservation
from SmartCampusBooking.use_cases.track_reservation import TrackReservation
from SmartCampusBooking.use_cases.view_facilities import ViewFacilities


def build_sample_users():
    return [
        User(1, "Ava Patel", "ava.patel@campus.edu", UserRole.STUDENT_REPRESENTATIVE, "Student Government"),
        User(2, "Marcus Lee", "marcus.lee@campus.edu", UserRole.FACULTY_STAFF, "Computer Science"),
        User(3, "Priya Shah", "priya.shah@campus.edu", UserRole.FACILITY_COORDINATOR, "Campus Operations"),
        User(4, "Daniel Kim", "daniel.kim@campus.edu", UserRole.EVENT_APPROVER, "Student Affairs"),
        User(5, "Rachel Gomez", "rachel.gomez@campus.edu", UserRole.SYSTEM_ADMINISTRATOR, "Administration"),
    ]


def build_sample_facilities():
    return [
        Facility(
            facility_id=101,
            name="Innovation Hall",
            location="North Campus",
            capacity=120,
            room="Room 204",
            facility_type="Lecture Hall",
            available=True,
            description="Large lecture room with projector and smart board.",
        ),
        Facility(
            facility_id=102,
            name="Sunset Atrium",
            location="Central Campus",
            capacity=60,
            room="Atrium A",
            facility_type="Event Space",
            available=True,
            description="Open event space for student gatherings and workshops.",
        ),
        Facility(
            facility_id=103,
            name="Greenfield Lab",
            location="Science Building",
            capacity=30,
            room="Lab 5",
            facility_type="Laboratory",
            available=True,
            description="Lab equipment ready for research and technical demos.",
        ),
    ]


def select_user(users):
    print("\nAvailable users:")
    for user in users:
        print(f"{user.user_id}. {user.name} ({user.role.value})")

    while True:
        try:
            user_id = int(input("Select user ID: ").strip())
            for user in users:
                if user.user_id == user_id:
                    return user
            print("User ID not found. Please choose a valid ID.")
        except ValueError:
            print("Please enter a valid numeric user ID.")


def main():
    users = build_sample_users()
    facility_manager = FacilityManager(build_sample_facilities())
    event_manager = EventManager()

    view_facilities = ViewFacilities(facility_manager)
    submit_reservation = SubmitReservation(facility_manager, event_manager)
    track_reservation = TrackReservation(event_manager)
    approve_reject = ApproveRejectReservation(event_manager)
    cancel_reservation = CancelReservation(event_manager)

    while True:
        print("\n========================================")
        print("    SMART CAMPUS BOOKING SYSTEM")
        print("========================================")
        print("1. View Available Facilities")
        print("2. Submit Reservation Request")
        print("3. Track Reservation Status")
        print("4. Approve or Reject Reservation")
        print("5. Cancel Reservation")
        print("6. Exit")

        choice = input("Select an option: ").strip()

        try:
            if choice == "1":
                view_facilities.run()
            elif choice == "2":
                requester = select_user(users)
                submit_reservation.run(requester)
            elif choice == "3":
                requester = select_user(users)
                track_reservation.run(requester)
            elif choice == "4":
                approver = select_user(users)
                approve_reject.run(approver)
            elif choice == "5":
                requester = select_user(users)
                cancel_reservation.run(requester)
            elif choice == "6":
                print("Exiting Smart Campus Booking System.")
                break
            else:
                print("Invalid menu selection. Please choose a number from 1 to 6.")
        except Exception as exc:
            print(f"An unexpected error occurred: {exc}")


if __name__ == "__main__":
    main()
