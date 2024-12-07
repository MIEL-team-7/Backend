from passlib.context import CryptContext


# Настраиваем контекст для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Функция для хеширования пароля
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# Функция для проверки пароля
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
