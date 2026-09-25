from serve.features.authentication.common.generator_code_handler import generate_code

def test_generate_code_returns_six_digits():
    otp = generate_code()

    assert len(otp) == 6
    assert otp.isdigit()


def test_generate_code_generates_different_codes():
    otp = {generate_code() for _ in range(100)}

    assert len(otp) > 1