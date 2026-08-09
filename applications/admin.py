from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.html import format_html

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


class ZeroPointsFilter(admin.SimpleListFilter):
    title = "pontuação"
    parameter_name = "pontuacao"

    def lookups(self, request, model_admin):
        return (
            ("zero", "Chegou a 0 pontos"),
            ("sem_pontos", "Ainda sem pontos atribuídos"),
        )

    def queryset(self, request, queryset):
        if self.value() == "sem_pontos":
            return queryset.filter(points_baseline__isnull=True)

        if self.value() == "zero":
            ids = [
                p.pk for p in queryset.filter(points_baseline__isnull=False)
                if p.current_points == 0
            ]
            return queryset.filter(pk__in=ids)

        return queryset


@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "edition",
        "status",
        "points_display",
        "accepted_at",
    )

    list_filter = (
        "edition",
        "status",
        ZeroPointsFilter,
    )

    search_fields = (
        "user__email",
        "user__first_name",
        "user__last_name",
    )

    readonly_fields = (
        "current_points_display",
    )

    def points_display(self, obj):
        if obj.points_baseline is None:
            return "—"

        if obj.current_points == 0:
            return format_html(
                '<strong style="color:#d62828">⚠ 0 / {}</strong>',
                obj.points_baseline,
            )

        return f"{obj.current_points} / {obj.points_baseline}"

    points_display.short_description = "Pontos"

    def current_points_display(self, obj):
        if obj.points_baseline is None:
            return "Ainda sem pontos atribuídos (a edição não está 'A decorrer')."

        return f"{obj.current_points} de {obj.points_baseline} pontos iniciais."

    current_points_display.short_description = "Pontuação atual"