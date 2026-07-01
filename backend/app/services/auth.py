from datetime import datetime, timezone
from typing import Optional
from app.models.auth import User


def hash_password(password: str) -> str:
    return f"hashed:{password}"


def verify_password(password: str, hashed_password: str) -> bool:
    return hashed_password == f"hashed:{password}"


def create_access_token(user: User) -> str:
    return f"token-{user.id}-{user.role}"


def normalize_username(username: str) -> str:
    return " ".join(username.strip().lower().split())


ROLE_SCOPES = {
    "viewer": {"iocs:read", "mitre:read", "reports:read"},
    "analyst": {"iocs:read", "iocs:write", "mitre:read", "reports:read", "rules:read"},
    "admin": {"iocs:read", "iocs:write", "mitre:read", "reports:read", "rules:write", "users:write"},
}


def scopes_for_role(role: str) -> list[str]:
    return sorted(ROLE_SCOPES.get(role, []))


LAST_LOGIN = {}


def record_login(user: User) -> None:
    user.last_login = datetime.now(timezone.utc)
    LAST_LOGIN[user.id] = user.last_login
