import os
from email.message import EmailMessage

import aiosmtplib
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

async def send_email(
    recipient: str,
    subject: str,
    html: str,
) -> None:
    if not recipient:
        logger.warning("Email recipient is empty")
        return

    try:
        message = EmailMessage()

        message["From"] = os.environ["MAILER_FROM"]
        message["To"] = recipient
        message["Subject"] = subject

        message.set_content(
            "This email requires an HTML-compatible email client."
        )
        message.add_alternative(html, subtype="html")

        await aiosmtplib.send(
            message,
            hostname=os.environ["MAILER_HOST"],
            port=int(os.environ["MAILER_PORT"]),
            username=os.environ["MAILER_USERNAME"],
            password=os.environ["MAILER_PASSWORD"],
            start_tls=True,
        )

        logger.success(
            "Email sent successfully to {} with subject '{}'",
            recipient,
            subject,
        )

    except Exception as exception:
        logger.error(
            "Failed to send email to {}: {}",
            recipient,
            exception,
        )
        raise