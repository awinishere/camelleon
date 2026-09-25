from serve.features.authentication.common.hashing_handler import hashing
from serve.features.authentication.common.match_handler import match


def test_match_correct_password():
    password = "password123"
    hashed_password = hashing(password)

    assert match(password, hashed_password) is True


def test_match_incorrect_password():
    password = "password123"
    wrong_password = "wrong-password"
    hashed_password = hashing(password)

    assert match(wrong_password, hashed_password) is False