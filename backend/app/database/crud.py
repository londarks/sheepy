import utilities as  schemas
from sqlalchemy.orm import Session
from . import models
from typing import Dict, Optional
from datetime import datetime, timedelta


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


def get_tokens_by_email(db: Session, user_id: int) -> Optional[Dict[str, str]]:
    """
    Busca os tokens de acesso e atualização do usuário pelo seu ID.
    :param db: objeto da sessão do banco de dados.
    :param email: ID do usuário cujos tokens serão buscados.
    :return: Um dicionário contendo os tokens de acesso e atualização, ou None se o usuário não tiver tokens.
    """
    tokens = db.query(models.Token).filter(models.Token.user_id == user_id).first()
    if not tokens:
        return None
    return {'access_token': tokens.access_token, 'refresh_token': tokens.refresh_token}


def update_access_token(db: Session, user_id: str, new_token: str, refresh_token: str) -> models.Token:
    """
    Atualiza o access token do usuário no banco de dados.

    :param db: objeto de sessão do banco de dados
    :param user_id: id do usuário
    :param new_token: novo token de acesso
    :param refresh_token: token de atualização
    :return: retorna o token atualizado
    """
    access_token = db.query(models.Token).filter(models.Token.user_id == user_id, models.Token.refresh_token == refresh_token).first()
    if not access_token:
        return None
    access_token.access_token = new_token
    access_token.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(access_token)
    return access_token


def update_refresh_token(db: Session, user_id: int, refresh_token: str) -> None:
    """
    Atualiza o refresh token do usuário no banco de dados.

    :param db: objeto de sessão do banco de dados
    :param user_id: id do usuário
    :param refresh_token: token de atualização
    """
    token = db.query(models.Token).filter_by(user_id=user_id, refresh_token=refresh_token).first()
    if token is not None:
        token.refresh_token = schemas.TokenCreate.refresh_token()
        token.updated_at = datetime.utcnow()
        db.commit()



def create_product(db: Session, product: schemas.ProductBase):
    """
    Create a new product and add it to the database.

    Args:
        db (Session): The database session.
        product (schemas.ProductBase): The product data.

    Returns:
        models.Product: The newly created product.
    """
    db_product = models.Product(name=product.name, description=product.description,
                         price=product.price, quantity=product.quantity,
                         image=product.image)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product