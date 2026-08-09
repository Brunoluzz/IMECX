from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("sobre/", views.about, name="about"),
    path("contacto/", views.contact, name="contact"),
    path("ficheiros/<path:path>/", views.secure_media, name="secure_media"),
]
