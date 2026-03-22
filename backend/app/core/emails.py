import logging
from pathlib import Path
from typing import Any, Dict

import emails
from emails.template import JinjaTemplate

from app.core.config import settings

def send_email(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: Dict[str, Any] = {},
) -> None:
    assert settings.EMAILS_FROM_EMAIL, "no provided email"
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    response = message.send(to=email_to, render=environment, smtp=smtp_options)
    logging.info(f"send email result: {response}")

def send_invitation_email(email_to: str, token: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Invitation to register"
    base_url = settings.FRONTEND_URL.rstrip('/')
    link = f"{base_url}/register?token={token}"
    html = f"""
    <p>You have been invited to join the {project_name} platform.</p>
    <p>Click the link below to set up your account and start using the autograder:</p>
    <p><a href="{link}">{link}</a></p>
    <p>This link will expire in a few days.</p>
    """
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=html,
    )
