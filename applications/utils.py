from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
import requests


def send_account_activation_email(user, edition):

    uid = urlsafe_base64_encode(
        force_bytes(user.pk)
    )

    token = default_token_generator.make_token(user)

    reset_url = (
        f"{settings.SITE_URL}"
        f"{reverse(
            'password_reset_confirm',
            kwargs={
                'uidb64': uid,
                'token': token
            }
        )}"
    )

    subject = render_to_string(
        "registration/set_password_subject.txt"
    ).strip()

    html_content = render_to_string(
        "registration/set_password_email.html",
        {
            "user": user,
            "edition": edition,
            "reset_url": reset_url,
        }
    )

    response = requests.post(
        "https://api.brevo.com/v3/smtp/email",
        headers={
            "accept": "application/json",
            "api-key": settings.BREVO_API_KEY,
            "content-type": "application/json",
        },
        json={
            "sender": {
                "name": "IMECX",
                "email": settings.DEFAULT_FROM_EMAIL,
            },
            "to": [
                {
                    "email": user.email,
                }
            ],
            "subject": subject,
            "htmlContent": html_content,
        },
        timeout=10,
    )

    response.raise_for_status()