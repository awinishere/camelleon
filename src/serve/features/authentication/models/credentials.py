from datetime import datetime

from sqlalchemy import DateTime, Enum as SqlEnum, String, func
from sqlalchemy.orm import Mapped, mapped_column

from serve.database import Base
from serve.features.authentication.models.extensions.type_roles import Roles

class Credentials(Base):
    __tablename__ = "credentials"

    id: Mapped[int] =  mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )
    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    role: Mapped[Roles] = mapped_column(
        SqlEnum(Roles),
        default=Roles.User,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )