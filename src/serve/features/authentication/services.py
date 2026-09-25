from datetime import datetime, timedelta, timezone

from loguru import logger
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from serve.features.authentication.common.generator_code_handler import generate_code
from serve.features.authentication.common.hashing_handler import hashing
from serve.features.authentication.models.credentials import Credentials
from serve.features.authentication.models.extensions.type_purpose import TypePurpose
from serve.features.authentication.models.extensions.type_roles import Roles
from serve.features.authentication.models.otp import OTP
from serve.features.authentication.schema.verification_email import VerificationEmailRequest
from serve.shared.common.template_handler import render_template
from serve.shared.email.send_email_handler import send_email


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

async def send_verification_otp(
        session: AsyncSession,
        credentials: Credentials,
) -> None:
    now = datetime.now(timezone.utc)
    window_start = now - timedelta(minutes=15)

    send_count = await session.scalar(
        select(func.count(OTP.id)).where(
            OTP.credentials_id == credentials.id,
            OTP.purpose == TypePurpose.Email_Verification,
            OTP.created_at >= window_start,
        )
    )


    if send_count >= 3:
        raise ValueError(
            "Maximum OTP request reached. Please try again later"
        )

    code = generate_code()

    otp = OTP(
        credentials_id=credentials.id,
        code=code,
        purpose=TypePurpose.Email_Verification,
        expires_at=now + timedelta(minutes=5),
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    session.add(otp)
    await session.flush()
    html = render_template("email/otp.html", otp=code)

    await send_email(
        recipient=credentials.email,
        subject="Email Verification",
        html=html
    )

async def verification_otp(
    session: AsyncSession,
    request: VerificationEmailRequest,
) -> Credentials:
    credentials = await session.scalar(
        select(Credentials).where(
            Credentials.email == request.email,
        )
    )

    if credentials is None:
        raise ValueError("Credentials not found")

    otp = await session.scalar(
        select(OTP)
        .where(
            OTP.credentials_id == credentials.id,
            OTP.code == request.code_otp,
            OTP.purpose == TypePurpose.Email_Verification,
        )
        .order_by(OTP.created_at.desc())
    )

    if otp is None:
        raise ValueError("Invalid OTP")

    if otp.expires_at <= datetime.now(timezone.utc):
        raise ValueError("OTP has expired")

    credentials.active = True

    await session.delete(otp)
    await session.commit()
    await session.refresh(credentials)

    logger.success(
        "Email verification successful: credentials_id={}",
        credentials.id,
    )

    return credentials