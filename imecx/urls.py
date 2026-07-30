from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("conta/", include("allauth.urls")),
    path("conta/", include("accounts.urls")),
    path("edicoes/", include("editions.urls")),
    path("candidaturas/", include("applications.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("", include("core.urls")),
    path("tasks/", include("tasks.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
