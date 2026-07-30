from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import View
from django.views.generic import TemplateView
from .forms import ProfileUpdateForm, UserUpdateForm
from .mixins import EmailVerifiedMixin
from django.views.generic import TemplateView
from applications.models import Participation
from editions.models import Edition


class ProfileEditView(LoginRequiredMixin, EmailVerifiedMixin, View,):
    template_name = "accounts/profile_edit.html"
    login_url = "account_login"

    def get(self, request):
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        return render(request, self.template_name, {
            "user_form": user_form,
            "profile_form": profile_form,
        })

    def post(self, request):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Perfil atualizado com sucesso.")
            return redirect("accounts:profile_edit")
        return render(request, self.template_name, {
            "user_form": user_form,
            "profile_form": profile_form,
        })
    
class ParticipantDashboardView(LoginRequiredMixin, EmailVerifiedMixin, TemplateView,):
    template_name = "accounts/area_pessoal.html"
    login_url = "account_login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        context["applications"] = (
            user.applications
            .select_related("edition", "area")
            .order_by("-created_at")
        )

        context["current_participation"] = (
            Participation.objects
            .filter(
                user=user,
                status="active",
                edition__status="active"
            )
            .select_related("edition")
            .first()
        )

        context["past_participations"] = (
            Participation.objects
            .filter(
                user=user,
                edition__status="finished"
            )
            .select_related("edition")
            .order_by("-edition__year")
        )

        return context
    
class EmailVerificationRequiredView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/email_verification_required.html"
    login_url = "account_login"