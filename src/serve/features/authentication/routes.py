from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from serve.database import get_database
from serve.features.authentication.schema.register import (
    RegisterRequest,
    RegisterResponse,
)
from serve.features.authentication.schema.verification_email import (
    VerificationEmailRequest,
    VerificationEmailResponse,
)
from serve.features.authentication.services import (
    register,
    verification_otp,
)

router = APIRouter(
    prefix="/api/v1/authentication",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_route(
    request: RegisterRequest,
    session: AsyncSession = Depends(get_database),
) -> RegisterResponse:
    try:
        credentials = await register(
            session=session,
            email=request.email,
            password=request.password,
        )

        return RegisterResponse(
            id=credentials.id,
            email=credentials.email,
            role=credentials.role.value,
        )

    except ValueError as exception:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exception),
        )


@router.post(
    "/verification",
    response_model=VerificationEmailResponse,
    status_code=status.HTTP_200_OK,
)
async def verification_email_route(
    request: VerificationEmailRequest,
    session: AsyncSession = Depends(get_database),
) -> VerificationEmailResponse:
    try:
        await verification_otp(
            session=session,
            request=request,
        )

        return VerificationEmailResponse(
            message="Email verification successful",
        )

    except ValueError as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exception),
        )