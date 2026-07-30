from allauth.account.models import EmailAddress


def resend_confirmation_email(request):
    email = EmailAddress.objects.filter(
        user=request.user,
        primary=True,
    ).first()

    if email and not email.verified:
        email.send_confirmation(request)