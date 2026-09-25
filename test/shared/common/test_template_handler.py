from serve.shared.common.template_handler import render_template


def test_render_template():
    result = render_template(
        "email/otp.html",
        otp="123456",
    )

    assert "<strong>123456</strong>" in result
    assert "{{ otp }}" not in result


def test_render_template_returns_html():
    result = render_template(
        "email/otp.html",
        otp="123456",
    )

    assert isinstance(result, str)
    assert "<html" in result
    assert "</html>" in result