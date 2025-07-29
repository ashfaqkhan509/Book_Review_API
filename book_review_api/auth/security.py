from datetime import datetime, timedelta, timezone
import jwt
from passlib.context import CryptContext
from decouple import config


SECRET_KEY = str(config("SECRET_KEY"))
ALGORITHM = str(config("ALGORITHM"))
ACCESS_TOKEN_EXPIRE_MINUTES = int(config("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Password hashing context
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify that a plain password matches the hashed password.

    Args:
        plain_password: The plain text password.
        hashed_password: The hashed password stored in the database.

    Returns:
        True if the password matches, False otherwise.
    """
    return password_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a plain password using bcrypt.

    Args:
        password: The plain text password.

    Returns:
        The hashed password as a string.
    """
    return password_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Create a JWT access token.

    Args:
        data: A dictionary containing the token payload.
        expires_delta: Optional expiration time for the token. Defaults to 15 minutes.

    Returns:
        A JWT token as a string.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta if expires_delta else timedelta(minutes=15)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
