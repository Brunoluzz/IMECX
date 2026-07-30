from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import (
    Application,
    EngineeringArea,
    Participation,
)

User = get_user_model()


@admin.action(description="Aceitar candidaturas selecionadas")
def accept_applications(modeladmin, request, queryset):

    for application in queryset:
        application.status = "accepted"
        application.save()


@admin.register(EngineeringArea)
class EngineeringAreaAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):

    actions = [accept_applications]

    list_display = (
        "full_name",
        "email",
        "edition",
        "area",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "edition",
        "area",
    )

    search_fields = (
        "full_name",
        "email",
        "university",
    )

    list_editable = (
        "status",
    )

    autocomplete_fields = (
        "edition",
        "area",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "edition",
        "status",
        "accepted_at",
    )

    list_filter = (
        "edition",
        "status",
    )

    search_fields = (
        "user__email",
        "user__first_name",
        "user__last_name",
    )