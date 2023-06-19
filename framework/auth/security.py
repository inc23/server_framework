from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


p = get_password_hash('230588')
print(p)
print(verify_password('230588', '$2b$12$m53cbACrcAkJU2fRflnkAuTG0Yxf1ijNLA8LbIhwR.52Zrf2U4iEm'))