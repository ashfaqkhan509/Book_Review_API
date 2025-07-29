from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Annotated
from database import engine, Base, get_db
from auth.models import User as UserModel
from auth.schemas import User, UserCreate, Token
from auth.dependencies import authenticate_user, get_current_user
from auth.security import (
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_password_hash,
)
from books.routes import router as books_router


# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Book Review Platform API")


@app.post("/register", response_model=User)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user in the system.

    Args:
        user (UserCreate): User data including username, full name, email, password, and admin flag.
        db (Session): SQLAlchemy session for database access.

    Raises:
        HTTPException: If the username is already registered.

    Returns:
        User: Created user record.
    """

    existing_user = (
        db.query(UserModel).filter(UserModel.username == user.username).first()
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = get_password_hash(user.password)
    db_user = UserModel(
        username=user.username,
        full_name=user.full_name,
        email=user.email,
        hashed_password=hashed_password,
        is_admin=user.is_admin,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    """
    Authenticate a user and generate a JWT access token.

    Args:
        form_data (OAuth2PasswordRequestForm): User login credentials (username and password).
        db (Session): SQLAlchemy session for database access.

    Raises:
        HTTPException: If authentication fails.

    Returns:
        Token: JWT access token and token type.
    """

    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    """
    Retrieve the currently authenticated user's details.

    Args:
        current_user (User): Current user obtained from the JWT token.

    Returns:
        User: Current authenticated user's information.
    """
    return current_user


# Include book and review endpoints
app.include_router(books_router)
