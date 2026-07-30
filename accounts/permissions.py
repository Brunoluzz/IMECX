from allauth.account.models import EmailAddress


def has_verified_email(user):
    """
    True caso o utilizador tenha um email
    primário confirmado.
    """

    if not user.is_authenticated:
        return False

    return EmailAddress.objects.filter(
        user=user,
        verified=True,
        primary=True,
    ).exists()


def can_access_private_area(user):
    """
    Pode aceder às áreas privadas do IMECX.
    """

    return has_verified_email(user)