from enum import Enum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    phone_number: Mapped[str] = mapped_column(unique=True)

    addresses: Mapped["Message"] = relationship(back_populates="user")


# class MessageDirection:
# INCOMING = "incoming"
# OUTGOING = "outgoing"


class Message(Base):
    __tablename__ = "message"
    id: Mapped[int] = mapped_column(primary_key=True)
    message: Mapped[str]
    direction: Mapped[Enum]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    addresses: Mapped["User"] = relationship(back_populates="message")
