from datetime import datetime, timedelta, timezone
from pathlib import Path

import jwt


PRIVATE_KEY_PATH = (
    Path(__file__).resolve().parents[2] / "keys" / "privateKey.pem"
)

with PRIVATE_KEY_PATH.open("r") as file:
    PRIVATE_KEY = file.read()


def generate_access_token(
    credentials_id: int,
    role: str,
) -> str:
    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(credentials_id),
        "role": role,
        "type": "access",
        "iat": now,
        "exp": now + timedelta(minutes=15),
    }

    return jwt.encode(
        payload,
        PRIVATE_KEY,
        algorithm="RS256",
    )


def generate_refresh_token(
    credentials_id: int,
) -> str:
    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(credentials_id),
        "type": "refresh",
        "iat": now,
        "exp": now + timedelta(days=30),
    }

    return jwt.encode(
        payload,
        PRIVATE_KEY,
        algorithm="RS256",
    )