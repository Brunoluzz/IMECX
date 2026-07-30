from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from applications.models import Participation

from allauth.account.models import EmailAddress

from .models import Profile

User = get_user_model()

# Remover o UserAdmin registado pelo Django
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass


class EmailVerifiedFilter(admin.SimpleListFilter):
    title = "Email confirmado"
    parameter_name = "email_verified"

    def lookups(self, request, model_admin):
        return (
            ("yes", "Sim"),
            ("no", "Não"),
        )

    def queryset(self, request, queryset):
        verified_ids = EmailAddress.objects.filter(
            verified=True
        ).values_list("user_id", flat=True)

        if self.value() == "yes":
            return queryset.filter(id__in=verified_ids)

        if self.value() == "no":
            return queryset.exclude(id__in=verified_ids)

        return queryset


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "verified",
        "role",
        "created_at",
        "phone",
    )

    list_filter = (
        "role",
    )

    list_editable = (
    )

    list_select_related = (
        "user",
    )

    date_hierarchy = "created_at"

    search_fields = (
        "user__email",
        "user__first_name",
        "user__last_name",
        "phone",
    )

    def verified(self, obj):
        return EmailAddress.objects.filter(
            user=obj.user,
            verified=True,
        ).exists()

    verified.boolean = True
    verified.short_description = "Email confirmado"

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ()

        return ("role",)


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    extra = 0
    readonly_fields = ()

    fields = (
        "phone",
        "bio",
        "role",
        "avatar_color",
    )

@admin.register(User)
class IMECXUserAdmin(UserAdmin):

    ordering = ("-date_joined",)

    list_display = (
        "email",
        "first_name",
        "last_name",
        "email_verified",
        "participations_count",
        "is_active",
        "is_staff",
        "last_login",
        "date_joined",
    )

    list_filter = (
        EmailVerifiedFilter,
        "is_active",
        "is_staff",
        "is_superuser",
    )

    search_fields = (
        "email",
        "first_name",
        "last_name",
    )

    readonly_fields = (
        "last_login",
        "date_joined",
    )

    inlines = [ProfileInline]

    def email_verified(self, obj):
        return EmailAddress.objects.filter(
            user=obj,
            verified=True,
        ).exists()

    email_verified.boolean = True
    email_verified.short_description = "Email confirmado"

    def participant(self, obj):
        return Participation.objects.filter(
            user=obj
        ).exists()

    def participations_count(self, obj):
        return obj.participations.count()

    participations_count.short_description = "Participações"
    participant.boolean = True
    participant.short_description = "Participante"