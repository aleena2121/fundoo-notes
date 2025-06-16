import smtplib
from email.mime.text import MIMEText

from app.config.logger import func_logger
from app.config.settings import smtpSettings


def send_verification_email(email: str, token: str):
    try:
        if not all(
            [
                smtpSettings.SMTP_SERVER,
                smtpSettings.SMTP_PORT,
                smtpSettings.SMTP_USERNAME,
                smtpSettings.SMTP_PASSWORD,
            ]
        ):
            raise ValueError("SMTP settings are incomplete")

        msg = MIMEText(
            f"Verify your email: {smtpSettings.BACKEND_URL}/verify-email?token={token}"
        )
        msg["Subject"] = "Verify Your Email"
        msg["From"] = smtpSettings.EMAIL_FROM
        msg["To"] = email

        with smtplib.SMTP(smtpSettings.SMTP_SERVER, smtpSettings.SMTP_PORT) as server:
            server.starttls()
            func_logger.debug(
                f"Attempting to login with username: {smtpSettings.SMTP_USERNAME}"
            )
            server.login(smtpSettings.SMTP_USERNAME, smtpSettings.SMTP_PASSWORD)
            server.send_message(msg)
            func_logger.info(f"Verification email sent to {email}")

    except smtplib.SMTPAuthenticationError as e:
        func_logger.error(e)
        raise
    except Exception as e:
        func_logger.error(f"Email sending failed: {str(e)}")
        raise


def send_expiration_email(to: str, subject: str, body: str):
    sender = smtpSettings.SMTP_USERNAME
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = to

    try:
        with smtplib.SMTP(smtpSettings.SMTP_SERVER, smtpSettings.SMTP_PORT) as server:
            server.starttls()
            func_logger.debug(
                f"sending mail to {sender}"
            )
            server.login(smtpSettings.SMTP_USERNAME, smtpSettings.SMTP_PASSWORD)
            server.send_message(msg)
            func_logger.info(f"email sent to {sender}")

    except smtplib.SMTPAuthenticationError as e:
        func_logger.error(e)
        raise
    except Exception as e:
        func_logger.error(f"Email sending failed: {str(e)}")
        raise