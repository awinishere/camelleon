from serve.features.authentication.common.hashing_handler import hashing


def test_hashing_password():
    password = "password1234"
    hashing_password = hashing(password)