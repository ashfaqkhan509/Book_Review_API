from sqlalchemy import String, Integer, Float, ForeignKey, Table, Text, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from auth.models import User

# association table for likes
review_likes = Table(
    "review_likes",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("review_id", Integer, ForeignKey("reviews.id"), primary_key=True)
)


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(150), index=True)
    author: Mapped[str] = mapped_column(String(100))

    reviews: Mapped[list["Review"]] = relationship("Review", back_populates="book", cascade="all, delete-orphan")


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    content: Mapped[str] = mapped_column(Text)
    rating: Mapped[float] = mapped_column(Float)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    book: Mapped["Book"] = relationship("Book", back_populates="reviews")
    owner: Mapped["User"] = relationship("User", back_populates="reviews")
    likes: Mapped[list["User"]] = relationship(
        "User",
        secondary=review_likes,
        back_populates="liked_reviews"
    )
