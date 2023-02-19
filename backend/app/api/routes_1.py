import logging
from utilities import  UserCreate, Login, create_user, login_user, ProductBase, register_production, updated_product
from fastapi import APIRouter, Depends, status, Response
from core import jwt_token_required, get_database_session, check_jwt_token


logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

router = APIRouter()

@router.get("/", tags=["Home"])
@jwt_token_required
async def home(payload: dict):
    return {"message": "This is a Flask API."}

@router.post("/auth/login", tags=["Auth"])
async def login(response: Response, register: Login, db: str = Depends(get_database_session)):
    """
    Autentica o usuário e retorna um token JWT.

    Args:
        response (Response): Objeto de resposta HTTP.
        register (Login): Objeto Pydantic que contém as credenciais do usuário.
        db (Session): Sessão do banco de dados.

    Returns:
        dict: Dicionário contendo o token JWT.

    Raises:
        HTTPException: Se as credenciais do usuário estiverem incorretas ou a conta estiver inativa.
    """
    token = login_user(database=db, user=register, response=response)
    return token


@router.post("/signup",status_code=status.HTTP_201_CREATED, tags=["Auth"])
async def register(response: Response, register: UserCreate, Database: str = Depends(get_database_session)):
    """
    Endpoint responsável pelo registro de um novo usuário na plataforma.

    Args:
        response (fastapi.Response): Objeto de resposta HTTP.
        register (UserCreate): Dados do usuário a ser registrado.
        Database (Session): Sessão do banco de dados.

    Returns:
        dict: Dicionário contendo o token de acesso gerado para o usuário recém-criado.

    Raises:
        HTTPException: Exceção HTTP com detalhes do erro caso haja algum problema durante a criação do usuário.
    """
    token = create_user(database=Database, user=register, response=response)
    return token


@router.post("/products",status_code=status.HTTP_201_CREATED,tags=["Products"])
def create_product(product: ProductBase, Database: str = Depends(get_database_session)):
    """
    Cria um novo produto no banco de dados.

    Parameters:
    -----------
    product: ProductBase
        Informações do produto a ser cadastrado.

    db: Session
        Conexão com o banco de dados.

    Returns:
    --------
    dict
        Informações do produto criado.
    """
    try:
        response = register_production(database=Database,product=product)
        return response
    except ValueError as e:
        return {'error': str(e)}
    except Exception as e:
        return {'error': str(e)}


@router.put("/products/{product_id}", tags=["Products"])
def update_product(product_id: int, product: ProductBase, Database: str = Depends(get_database_session)):
    """
    Atualiza um produto no banco de dados.

    Parameters:
    -----------
    product_id: int
        ID do produto a ser alterado.

    product: ProductBase
        Informações atualizadas do produto.

    db: Session
        Conexão com o banco de dados.

    Returns:
    --------
    dict
        Informações do produto atualizado.
    """
    try:
        response = updated_product(database=Database,product=product_id)
        return response
    except ValueError as e:
        return {'error': str(e)}
    except Exception as e:
        return {'error': str(e)}