from dataclasses import dataclass

from .enums import UserRole


@dataclass
class User:
    user_id: int
    name: str
    email: str
    role: UserRole
    organization: str = ""

    def display_info(self) -> str:
        organization_text = f" | Organization: {self.organization}" if self.organization else ""
        return (
            f"User ID: {self.user_id}\n"
            f"Name: {self.name}\n"
            f"Email: {self.email}\n"
            f"Role: {self.role.value}{organization_text}"
        )
