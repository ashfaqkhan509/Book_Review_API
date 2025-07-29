from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from auth.dependencies import get_current_user, get_current_admin_user
from database import get_db
from books import models, schemas
from auth.models import User
from sqlalchemy import func


router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/", response_model=schemas.Book)
def add_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
):
    """
    Add a new book to the database. Only accessible by admin users.

    Args:
        book (schemas.BookCreate): Book data.
        db (Session): Database session.
        current_admin (User): Current authenticated admin user.

    Returns:
        schemas.Book: The created book.
    """

    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@router.get("/", response_model=List[schemas.Book])
def list_books(
    db: Session = Depends(get_db),
    search: str = Query(None, description="Search books by title"),
    limit: int = Query(10, ge=1, le=100, description="Number of books to return"),
    offset: int = Query(0, ge=0, description="Number of books to skip"),
):
    """
    Retrieve a paginated list of books with optional title search.

    Args:
        db (Session): Database session.
        search (str, optional): Title filter (case-insensitive).
        limit (int): Max number of books per page (default 10).
        offset (int): Number of books to skip (default 0).

    Returns:
        List[schemas.Book]: Paginated list of books.
    """
    query = db.query(models.Book)
    if search:
        query = query.filter(models.Book.title.ilike(f"%{search}%"))
    return query.offset(offset).limit(limit).all()


@router.get("/{book_id}/average-rating")
def get_average_rating(book_id: int, db: Session = Depends(get_db)):
    """
    Get the average rating for a specific book by its ID.
    Returns 404 if the book does not exist or has no reviews.
    """
    avg_rating = (
        db.query(func.avg(models.Review.rating))
        .filter(models.Review.book_id == book_id)
        .scalar()
    )

    if avg_rating is None:
        raise HTTPException(
            status_code=404,
            detail="No ratings found for this book"
        )

    return {"book_id": book_id, "average_rating": round(avg_rating, 2)}


@router.post("/{book_id}/reviews", response_model=schemas.Review)
def add_review(
    book_id: int,
    review: schemas.ReviewBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Add a review to a specific book.

    Args:
        book_id (int): ID of the book to review.
        review (schemas.ReviewBase): Review data.
        db (Session): Database session.
        current_user (User): Current authenticated user.

    Returns:
        schemas.Review: The created review.
    """
    db_review = models.Review(
        **review.dict(), book_id=book_id, user_id=current_user.id
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


@router.post("/reviews/{review_id}/like")
def like_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Toggle like/unlike for a review by the current user.

    Args:
        review_id (int): ID of the review.
        db (Session): Database session.
        current_user (User): Current authenticated user.

    Returns:
        dict: Updated like count.
    """
    review = db.query(models.Review).get(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    if current_user in review.likes:
        review.likes.remove(current_user)
    else:
        review.likes.append(current_user)
    db.commit()
    return {"likes": len(review.likes)}


@router.delete("/{book_id}")
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
):
    """
    Delete a book by ID. Only accessible by admin users.

    Args:
        book_id (int): ID of the book to delete.
        db (Session): Database session.
        current_admin (User): Current authenticated admin user.

    Returns:
        dict: Success message.
    """
    book = db.query(models.Book).get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": "Book deleted"}
