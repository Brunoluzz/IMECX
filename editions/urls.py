from django.urls import path
from . import views

app_name = "editions"

urlpatterns = [
    path("", views.edition_list, name="list"),
    path("<int:year>/", views.edition_detail, name="detail"),
]
