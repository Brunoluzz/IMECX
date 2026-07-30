from allauth.account.adapter import DefaultAccountAdapter
from django.http import Http404


class IMECXAccountAdapter(DefaultAccountAdapter):

    def get_from_email(self):
        return "IMECX <projetomecanicacoimbra@gmail.com>"

    def format_email_subject(self, subject):
        return f"IMECX | {subject}"

    def is_open_for_signup(self, request):
        return False