from datetime import datetime, timedelta, timezone

import jwt

from serve.features.authentication.common.generate_token_handler import generate_access_token, generate_refresh_token


def test_generate_access_token():
    token = generate_access_token(
        credentials_id=1,
        role="User",
    )

    payload = jwt.decode(
        token,
        options={"verify_signature": False},
    )

    assert payload["sub"] == "1"
    assert payload["role"] == "User"
    assert payload["type"] == "access"
    assert "iat" in payload
    assert "exp" in payload


def test_generate_access_token_expires_in_15_minutes():
    token = generate_access_token(
        credentials_id=1,
        role="User",
    )

    payload = jwt.decode(
        token,
        options={"verify_signature": False},
    )

    iat = datetime.fromtimestamp(
        payload["iat"],
        timezone.utc,
    )

    exp = datetime.fromtimestamp(
        payload["exp"],
        timezone.utc,
    )

    assert timedelta(minutes=14, seconds=50) <= exp - iat
    assert exp - iat <= timedelta(minutes=15, seconds=10)


def test_generate_refresh_token():
    token = generate_refresh_token(
        credentials_id=1,
    )

    payload = jwt.decode(
        token,
        options={"verify_signature": False},
    )

    assert payload["sub"] == "1"
    assert payload["type"] == "refresh"
    assert "iat" in payload
    assert "exp" in payload


def test_generate_refresh_token_expires_in_30_days():
    token = generate_refresh_token(
        credentials_id=1,
    )

    payload = jwt.decode(
        token,
        options={"verify_signature": False},
    )

    iat = datetime.fromtimestamp(
        payload["iat"],
        timezone.utc,
    )

    exp = datetime.fromtimestamp(
        payload["exp"],
        timezone.utc,
    )

    assert timedelta(days=29, hours=23) <= exp - iat
    assert exp - iat <= timedelta(days=30, hours=1)