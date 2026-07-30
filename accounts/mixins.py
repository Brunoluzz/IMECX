from django.contrib import messages
from django.shortcuts import redirect

from .permissions import can_access_private_area


class EmailVerifiedMixin:

    def dispatch(self, request, *args, **kwargs):

        if not can_access_private_area(request.user):

            messages.warning(
                request,
                "Confirma primeiro o teu endereço de email para acederes a esta área."
            )

            return redirect("accounts:email_verification_required")

        return super().dispatch(request, *args, **kwargs)