import utilities as  schemas
from fastapi import Response
from sqlalchemy.orm import Session
from  sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
from core import PasswordManager, jwt_token_required, create_jwt_token, create_refresh_token
#core
from core import PasswordManager, is_token_expired
#typing
from typing import Dict, Union
#database
from database import models, crud


def login_user(database: Session, user: schemas.UserCreate, response: Response) -> Dict[str, str]:
    try:
        search = database.query(models.User).filter(models.User.email == user.email).first()
        if not search:
            raise ValueError("User not existed")

        password = PasswordManager.validate_password(password=user.password, hashed_password=search.password)

        if password:
            #pegar token salvo ou gerar um novo
            tokens = crud.get_tokens_by_email(db=database, user_id=search.id)
            
            if is_token_expired(token=tokens['access_token']) or is_token_expired(token=tokens['refresh_token']):
                tokens = update_tokens(database=database, user=search)
                response.set_cookie(key='refresh_token', value=tokens['refresh_token'], httponly=True)
                return {'access_token': tokens['access_token']}

            return {'message': 'Login sucess'}
        return {'message': 'Login fail'}
    except ValueError as e:
        response.status_code = 400
        return {'error': str(e)}
    except Exception as e:
        response.status_code = 500
        return {'error': "Internal server error"}

def create_user(database: Session, user: schemas.UserCreate, response: Response) -> Dict[str, str]:
    """
    Cria um novo usuário no banco de dados, incluindo a criação de tokens de acesso e atualização de informações na base de dados.

    :param database: objeto da sessão do banco de dados.
    :param user: objeto do tipo UserCreate contendo informações do novo usuário.
    :return: Um dicionário contendo um token de acesso.
    """
    try:
        search = database.query(models.User).filter(models.User.email == user.email).first()
        if search:
            raise ValueError("User already exists")
        user.password = PasswordManager.hash_password(password=user.password)
        crud.create_user(db=database, register=user)
        user = crud.get_user_by_email(db=database, email=user.email)
        token = create_jwt_token(user_id=user.id)
        refresh_token = create_refresh_token(user_id=user.id)
        crud.create_jwt(db=database, user_id=user.id, access_token=token, refresh_token=refresh_token)
        if isinstance(refresh_token, str):
            refresh_token = refresh_token.encode('utf-8')
        response.set_cookie(key='refresh_token', value=refresh_token.decode('utf-8'), httponly=True)
        return {'access_token': token}
    except ValueError as e:
        response.status_code = 400
        return {'error': str(e)}
    except SQLAlchemyError as e:
        response.status_code = 500
        return {'error': str(e)}


def update_tokens(database: Session, user: models.User) -> Dict[str, Union[str, Dict[str, str]]]:
    """
    Update access token and refresh token if they are expired, and return a dictionary containing the new access and
    refresh tokens.

    Args:
        database: database session object.
        user_id: the user ID.

    Returns:
        A dictionary containing the new access and refresh tokens.

    Raises:
        None
    """
    # Atualiza o access_token
    new_access_token = create_jwt_token(user.id)
    new_refresh_token = create_refresh_token(user.id)

    crud.update_access_token(db=database, user_id=user.id, new_token=new_access_token, refresh_token=new_refresh_token)
    database.commit()
    return {'access_token': new_access_token, 'refresh_token': new_refresh_token}



def register_production(database: Session, product: schemas.ProductBase):
    """
    Cadastra um novo produto no banco de dados, verificando se o item já existe.

    Args:
        database (Session): Sessão do banco de dados.
        product (ProductBase): Dados do produto a ser cadastrado.

    Returns:
        (Product) : Produto cadastrado no banco de dados.
    """

    # Verifica se o produto já existe no banco de dados.
    existing_product = database.query(models.Product).filter(models.Product.name == product.name).first()

    if existing_product:
        raise ValueError(status_code=400, detail="Produto já cadastrado")

    # Cadastra o produto no banco de dados.
    new_product = crud.create_product(db=database, product=product)

    return new_product