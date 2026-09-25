from datetime import datetime

from sqlalchemy import DateTime, Enum as SqlEnum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from serve.database import Base
from serve.features.authentication.models.extensions.type_purpose import TypePurpose


class OTP(Base):
    __tablename__ = "otps"

    id: Mapped[int] = mapped_column(primary_key=True)
    credentials_id: Mapped[int] = mapped_column(
        ForeignKey("credentials.id"),
        nullable=False,
    )
    code: Mapped[str] = mapped_column(
        String(6),
        nullable=False,
    )
    purpose: Mapped[TypePurpose] = mapped_column(
        SqlEnum(TypePurpose),
        nullable=False,
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
