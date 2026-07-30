from django.contrib import admin
from .models import Edition


@admin.register(Edition)
class EditionAdmin(admin.ModelAdmin):
    list_display = ("year", "theme", "status", "applications_open", "applications_close")
    list_filter = ("status",)
    search_fields = ("year", "theme")
    list_editable = ("status",)
    ordering = ("-year",)
