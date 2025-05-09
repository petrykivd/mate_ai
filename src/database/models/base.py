from datetime import datetime as dt
from uuid import UUID, uuid4

from sqlalchemy import DateTime, func
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()

class IdCreatedAtModelMixin:
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    created_at: Mapped[dt] = mapped_column(DateTime(timezone=True), default=func.now())
