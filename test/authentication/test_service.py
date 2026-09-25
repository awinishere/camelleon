from unittest.mock import AsyncMock, MagicMock

import pytest

from serve.features.authentication.models.credentials import Credentials
from serve.features.authentication.models.extensions.type_roles import Roles
from serve.features.authentication.services import register


@pytest.mark.asyncio
async def test_register_success():
    session = AsyncMock()
    session.scalar.return_value = None
    session.add = MagicMock()

    result = await register(
        session=session,
        email="user@example.com",
        password="password123",
    )

    created_credentials = session.add.call_args.args[0]

    assert isinstance(created_credentials, Credentials)
    assert created_credentials.email == "user@example.com"
    assert created_credentials.role == Roles.User
    assert created_credentials.password != "password123"

    session.add.assert_called_once()
    session.commit.assert_awaited_once()
    session.refresh.assert_awaited_once_with(created_credentials)

    assert result is created_credentials


@pytest.mark.asyncio
async def test_register_rejects_existing_email():
    session = AsyncMock()

    existing_credentials = Credentials(
        id=1,
        email="user@example.com",
        password="existing-hash",
        role=Roles.User,
    )

    session.scalar.return_value = existing_credentials
    session.add = MagicMock()

    with pytest.raises(ValueError, match="Email already registered"):
        await register(
            session=session,
            email="user@example.com",
            password="password123",
        )

    session.add.assert_not_called()
    session.commit.assert_not_awaited()
    session.refresh.assert_not_awaited()