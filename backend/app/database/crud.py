from sqlalchemy.orm import Session
from . import models
import utilities as  schemas


def get_all_user(db: Session):
    """ Get all user in database """
    users = db.query(models.User).all()
    if not users:
        raise ValueError("empty database")
    return users

def get_user_by_email(db: Session, email: str) -> models.User:
    """ Get user by id in database """
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise ValueError("User not in existsd")
    return user


def create_jwt(db: Session, user_id: int, access_token: str, refresh_token: str) -> models.Token:
    """Create a new JWT token and store it in the database.

    Args:
        session: The database session.
        user_id: The ID of the user associated with the token.
        access_token: The JWT access token.
        refresh_token: The JWT refresh token.

    Returns:
        The created token object.
    """
    try:
        token = models.Token(
            user_id=user_id,
            access_token=access_token,
            refresh_token=refresh_token
        )
        db.add(token)
        db.commit()
        db.refresh(token)
        return token
    except Exception as e:
        db.rollback()
        raise e

def create_user(db: Session, register: schemas.UserCreate) -> models.User:
    """Create a new user in the database.

    Args:
        db: The database session.
        register: The user registration information.

    Returns:
        The created user object.
    """
    db_user = models.User(
        name=register.name,
        address=register.address,
        email=register.email,
        phone=register.phone,
        password=register.password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
