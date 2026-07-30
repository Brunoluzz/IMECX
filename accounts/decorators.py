from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect

from .permissions import can_access_private_area


def email_verified_required(view):

    @wraps(view)
    def wrapper(request, *args, **kwargs):

        if not can_access_private_area(request.user):

            messages.warning(
                request,
                "Confirma primeiro o teu endereço de email."
            )

            return redirect("accounts:email_verification_required")

        return view(request, *args, **kwargs)

    return wrapper