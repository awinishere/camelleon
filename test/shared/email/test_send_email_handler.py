from unittest.mock import AsyncMock, patch

import pytest

from serve.shared.email import send_email_handler


@pytest.mark.asyncio
async def test_send_email_success(monkeypatch):
    monkeypatch.setenv("MAILER_FROM", "sender@example.com")
    monkeypatch.setenv("MAILER_HOST", "smtp.example.com")
    monkeypatch.setenv("MAILER_PORT", "587")
    monkeypatch.setenv("MAILER_USERNAME", "sender@example.com")
    monkeypatch.setenv("MAILER_PASSWORD", "password")

    with patch.object(
        send_email_handler.aiosmtplib,
        "send",
        new_callable=AsyncMock,
    ) as send:
        with patch.object(
            send_email_handler.logger,
            "success",
        ) as success:
            await send_email_handler.send_email(
                recipient="user@example.com",
                subject="Email Verification",
                html="<strong>123456</strong>",
            )

            send.assert_awaited_once()
            success.assert_called_once()


@pytest.mark.asyncio
async def test_send_email_warns_when_recipient_is_empty():
    with patch.object(
        send_email_handler.logger,
        "warning",
    ) as warning:
        await send_email_handler.send_email(
            recipient="",
            subject="Email Verification",
            html="<strong>123456</strong>",
        )

        warning.assert_called_once()


@pytest.mark.asyncio
async def test_send_email_logs_error_when_sending_fails(monkeypatch):
    monkeypatch.setenv("MAILER_FROM", "sender@example.com")
    monkeypatch.setenv("MAILER_HOST", "smtp.example.com")
    monkeypatch.setenv("MAILER_PORT", "587")
    monkeypatch.setenv("MAILER_USERNAME", "sender@example.com")
    monkeypatch.setenv("MAILER_PASSWORD", "password")

    with patch.object(
        send_email_handler.aiosmtplib,
        "send",
        new_callable=AsyncMock,
    ) as send:
        send.side_effect = RuntimeError("SMTP error")

        with patch.object(
            send_email_handler.logger,
            "error",
        ) as error:
            with pytest.raises(RuntimeError, match="SMTP error"):
                await send_email_handler.send_email(
                    recipient="user@example.com",
                    subject="Email Verification",
                    html="<strong>123456</strong>",
                )

            error.assert_called_once()