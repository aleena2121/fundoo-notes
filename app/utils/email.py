import smtplib
from email.mime.text import MIMEText

from app.config.logger import func_logger
from app.config.settings import *


def send_verification_email(email: str, token: str):
    try:
        if not all([SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD]):
            raise ValueError("SMTP settings are incomplete")

        msg = MIMEText(f"Verify your email: {BACKEND_URL}/verify-email?token={token}")
        msg["Subject"] = "Verify Your Email"
        msg["From"] = EMAIL_FROM
        msg["To"] = email

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            func_logger.debug(f"Attempting to login with username: {SMTP_USERNAME}")
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
            func_logger.info(f"Verification email sent to {email}")

    except smtplib.SMTPAuthenticationError as e:
        func_logger.error(e)
        raise
    except Exception as e:
        func_logger.error(f"Email sending failed: {str(e)}")
        raise
