from argon2 import PasswordHasher

plain_text = PasswordHasher()

def hashing(password: str) -> str:
    return plain_text.hash(password)
