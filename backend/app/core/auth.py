from fastapi import HTTPException, status, Request
from fastapi import  Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

import utilities as  schemas

from datetime import datetime, timedelta
from typing import Dict, Any, Union, Callable
import jwt

#database
from database import  crud
from database.connection import SessionLocal
from sqlalchemy.orm import Session

# Chave secreta usada para assinar o token JWT
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

# Duração do tempo de validade do token JWT (em minutos)
TOKEN_EXPIRATION_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 30

security = HTTPBearer()


def get_database_session() -> Session:
    """
    Retorna uma sessão de banco de dados para ser usada em um contexto com.

    Returns:
        Uma sessão de banco de dados.
    """ 
    database = SessionLocal()
    try:
        yield database
    finally:
        if not database.is_active:
            database.close()

def check_jwt_token(func: Callable):
    async def wrapper(request: Request, db: Session = Depends(get_database_session), **kwargs):
        try:
            token = request.headers.get('Authorization').split('Bearer ')[1]
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            if is_token_expired(token=token):

                tokens = schemas.update_tokens(database=db, user=payload['sub'])
                user_id = payload.get('sub')
                new_token = create_jwt_token(user_id)
                response = JSONResponse({'access_token': new_token})
                response.set_cookie(key='access_token', value=new_token, httponly=True, secure=True, max_age=1800)
                print("gerou um novo")
                return response
            
                #return await func(request, register)
            
        except Exception as e:
            print(e)
            #raise HTTPException(status_code=401, detail='Invalid token')
        print(kwargs)
        return await func(request, db, kwargs)

    return wrapper


# Decorator para verificar se o token JWT é válido
def jwt_token_required(func):
    async def wrapper(token: HTTPAuthorizationCredentials = Depends(security)):
        try:
            payload = verify_jwt_token(token.credentials)
            if not payload:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")
            return await func(payload)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    return wrapper


def create_jwt_token(user_id: int) -> str:
    """Cria um token JWT para o usuário especificado"""
    # Calcula a data e hora de expiração do token JWT
    expiration_time = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRATION_MINUTES)

    # Define as informações a serem incluídas no token JWT
    payload: Dict[str, Union[str, int, float]] = {"sub": str(user_id), "exp": expiration_time}

    # Cria e assina o token JWT usando a chave secreta
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return token


def create_refresh_token(user_id: int) -> str:
    """
    Cria um novo token de atualização para o usuário especificado.

    Args:
        user_id (int): ID do usuário.

    Returns:
        str: Token de atualização JWT codificado.
    """
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    payload: Dict[str, Union[str, int, float]] = {"sub": str(user_id), "exp": expire}
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def decode_token(token: str) -> Union[Dict[str, Union[str, int, float]], None]:
    """
    Decodifica um token JWT.

    Args:
        token (str): Token JWT codificado.

    Returns:
        Union[Dict[str, Union[str, int, float]], None]: Payload decodificado do token JWT, ou None em caso de erro.
    """
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded_token
    except jwt.exceptions.InvalidTokenError:
        return None



def is_token_expired(token: str) -> bool:
    """
    Verifica se um token JWT está expirado.

    Args:
        token (str): Token JWT codificado.

    Returns:
        bool: True se o token está expirado, False caso contrário.
    """
    decoded_token = decode_token(token)
    if decoded_token and 'exp' in decoded_token:
        exp_timestamp = decoded_token['exp']
        return datetime.utcnow() > datetime.fromtimestamp(exp_timestamp)
    return True


def refresh_access_token(token: str) -> Union[str, None]:
    """
    Renova um token de acesso JWT, gerando um novo com uma nova data de expiração.

    Args:
        token (str): Token JWT codificado.

    Returns:
        Union[str, None]: Novo token JWT de acesso codificado, ou None em caso de erro.
    """
    decoded_token = decode_token(token)
    if decoded_token:
        # Verifica se o token já expirou
        if is_token_expired(token):
            # Renova o token com uma nova data de expiração
            user_id = decoded_token['sub']
            new_token = create_jwt_token(user_id=user_id)
            return new_token
        else:
            # Se o token ainda não expirou, retorna o token original
            return token
    return None


def verify_jwt_token(token: str) -> Union[Dict[str, Any], None]:
    """Verifica se o token JWT foi emitido pelo servidor e retorna o payload se o token for válido"""
    try:
        # Verifica se o token JWT foi fornecido corretamente
        if not token or not token.startswith("Bearer "):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")

        token = token.split("Bearer ")[1]

        # Verifica a assinatura do token JWT usando a chave secreta
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        # Verifica a expiração do token JWT
        if datetime.utcfromtimestamp(payload["exp"]) < datetime.utcnow():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="expired token")

        # Retorna o payload se o token JWT for válido
        return payload
    except jwt.exceptions.InvalidSignatureError:
        # Retorna None se a assinatura do token JWT for inválida
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")