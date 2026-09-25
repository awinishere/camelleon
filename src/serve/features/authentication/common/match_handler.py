from argon2 import PasswordHasher

plain_text = PasswordHasher()

def match(password: str, password_hash: str) -> bool:
    try:
        plain_text.verify(password_hash, password)
        return True
    except Exception:
        return False