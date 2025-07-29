from pydantic import BaseModel
from typing import List


class ReviewBase(BaseModel):
    content: str
    rating: float


class ReviewCreate(ReviewBase):
    book_id: int


class Review(ReviewBase):
    id: int
    book_id: int
    user_id: int

    class Config:
        from_attributes = True


class BookBase(BaseModel):
    title: str
    author: str

class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int
    reviews: List[Review] = []

    class Config:
        from_attributes = True
