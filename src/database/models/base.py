from uuid import UUID, uuid4

from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()

class IdModelMixin:
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
