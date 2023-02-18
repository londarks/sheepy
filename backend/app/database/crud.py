from sqlalchemy.orm import Session
from . import models
import utilities as  schemas


def get_all_user(db: Session):
    """ Get all user in database """
    users = db.query(models.User).all()
    if not users:
        raise ValueError("empty database")
    return users

def get_user_by_email_register(db: Session, email: str) -> models.User:
    """ Get user by id in database """
    user = db.query(models.User).filter(models.User.email == email).first()
    if user:
        raise ValueError("User already existsd")
    return user

def get_user_by_email(db: Session, email: str) -> models.User:
    """ Get user by id in database """
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise ValueError("User not in existsd")
    return user


def create_jwt(db: Session, register: schemas.UserRegister) -> models.User:
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

def create_user(db: Session, register: schemas.UserRegister) -> models.User:
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
