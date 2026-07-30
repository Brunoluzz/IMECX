from django.shortcuts import render, get_object_or_404
from .models import Edition


def edition_list(request):
    editions = Edition.objects.all()
    return render(request, "editions/list.html", {"editions": editions})


def edition_detail(request, year):
    edition = get_object_or_404(Edition, year=year)
    return render(request, "editions/detail.html", {"edition": edition})
