from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "accounts"

urlpatterns = [
    path("area/", views.ParticipantDashboardView.as_view(), name="area_pessoal"),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path("verificar-email/", views.EmailVerificationRequiredView.as_view(), name="email_verification_required"),
]
