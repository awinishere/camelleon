from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from serve.features.authentication.common.hashing_handler import hashing
from serve.features.authentication.models.credentials import Credentials
from serve.features.authentication.models.extensions.type_roles import Roles


async def register( session: AsyncSession, email: str,password: str) -> Credentials:
    existing_credentials = await session.scalar(
        select(Credentials).where(Credentials.email == email)
    )

    if existing_credentials is not None:
        raise ValueError("Email already registered")

    credentials = Credentials(
        email = email,
        password = hashing(password),
        role = Roles.User,
    )

    session.add(credentials)

    await session.commit()
    await session.refresh(credentials)

    logger.success("Registration successful: credentials_id={}", credentials.id)
    return credentials

