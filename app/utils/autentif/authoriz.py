from fastapi.openapi.models import Response
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status, APIRouter
from pydantic import Field
from jose import jwt, JWTError
from datetime import datetime, timezone

from app.core.config import settings
from app.models.models import Manager
from app.schemas.manager_schema import getManager
from app.utils.autentif.passw import verify_password
from app.utils.autentif.tok import create_access_token, decode_token, get_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

auth_router = APIRouter(prefix="/auth", tags=["Авторизация"])

class ManagerAuth(getManager):
    email: str = Field(..., description="Электронная почта")
    password: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")

async def authenticate_user(email: str, password: str):
    user = await Manager.find_one_or_none(email=email)
    if not user or verify_password(plain_password=password, hashed_password=user.password) is False:
        return None
    return user


# Авторизация руководителя и создание токена
@auth_router.post("/login/")
async def login(response: Response, user_data: ManagerAuth):
    check = await authenticate_user(email=user_data.email, password=user_data.password)
    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Неверная почта или пароль')
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {'access_token': access_token, 'refresh_token': None}


# Защищённый маршрут
@auth_router.get("/protected/")
def protected_route(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(
            status_code=401, detail="Неверный токен или срок действия истёк"
        )

    return {"msg": f"Добро пожаловать, {payload['sub']}!"}


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен не валидный!')

    expire = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен истек')

    manager_id = payload.get('sub')
    if not manager_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Не найден ID Руководителя')

    user = await Manager.find_one_or_none_by_id(int(manager_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Руководитель не найден')

    return user


@auth_router.get("/me/")
async def get_me(user_data: Manager = Depends(get_current_user)):
    return user_data


@auth_router.post("/logout/")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {'message': 'Пользователь успешно вышел из системы'}
