from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
import requests

class IMECXAccountAdapter(DefaultAccountAdapter):

    def get_from_email(self):
        return "IMECX <projetomecanicacoimbra@gmail.com>"

    def format_email_subject(self, subject):
        return f"IMECX | {subject}"

    def is_open_for_signup(self, request):
        return False

    def send_mail(self, template_prefix, email, context):

        message = self.render_mail(
            template_prefix,
            email,
            context
        )

        html_content = None

        for content, mimetype in message.alternatives:
            if mimetype == "text/html":
                html_content = content
                break

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
                        "email": email,
                    }
                ],
                "subject": message.subject,
                "htmlContent": html_content or message.body,
            },
            timeout=10,
        )

        response.raise_for_status()