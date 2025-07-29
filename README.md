# Book Review Platform API

A backend API built with **FastAPI** that allows users to:

- Register and log in with JWT-based authentication.
- Add books (admin only).
- Post reviews on books.
- Like/dislike reviews.
- Get average ratings for books.
- Search and filter books.
- Use pagination for large book lists.

---

## Features

- **JWT Authentication** (login & register)
- **Role-based access** (admin and regular users)
- **SQLAlchemy ORM** with SQLite (easily switchable to PostgreSQL)
- **Pydantic validation** for request/response models
- **Books–Reviews–Likes relationships**
- **Pagination, filtering, and search**
- **Secure password hashing** with Passlib (bcrypt)

---

## Technologies Used

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/)
- [Pydantic](https://docs.pydantic.dev/)
- [Passlib](https://passlib.readthedocs.io/en/stable/) for password hashing
- [python-jose](https://python-jose.readthedocs.io/en/latest/) for JWT
- [python-decouple](https://pypi.org/project/python-decouple/) for environment variables

---

## Project Structure

book_review_api/
├── auth/
│ ├── models.py # User model
│ ├── schemas.py # Pydantic schemas
│ ├── security.py # Password hashing & JWT utilities
│ ├── dependencies.py # Authentication & admin dependencies
├── books/
│ ├── models.py # Book & Review models
│ ├── schemas.py # Pydantic schemas
│ ├── routes.py # Endpoints for books & reviews
├── database.py # DB engine, session, Base
├── main.py # FastAPI entry point
└── README.md


---

## Setup & Installation

1. **Clone the repository**:
    ```bash
    git clone git@github.com:ashfaqkhan509/Book_Review_API.git
    cd book-review-api
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set environment variables** (create a `.env` file):
    ```
    SECRET_KEY=your_secret_key
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```

5. **Run the app**:
    ```bash
    uvicorn main:app --reload
    ```

---
