from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """SQLAlchemy declarative base for all ORM models."""

    pass


class PetModel(Base):
    """ORM model for the pets table."""

    __tablename__ = "pets"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False, default="available")
    category: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    orders: Mapped[list["OrderModel"]] = relationship(
        back_populates="pet", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<PetModel(id={self.id}, name={self.name}, status={self.status})>"


class OrderModel(Base):
    """ORM model for the orders table."""

    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    pet_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("pets.id", ondelete="CASCADE"), nullable=False
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    status: Mapped[str] = mapped_column(String, nullable=False, default="placed")
    complete: Mapped[bool] = mapped_column(Boolean, default=False)
    ship_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    pet: Mapped["PetModel"] = relationship(back_populates="orders")

    def __repr__(self) -> str:
        return f"<OrderModel(id={self.id}, pet_id={self.pet_id}, status={self.status})>"
