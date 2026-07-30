from django.shortcuts import render
from django.contrib import messages
from editions.models import Edition
from applications.models import EngineeringArea


def home(request):
    editions = Edition.objects.all()[:3]
    areas = EngineeringArea.objects.all()[:6]
    return render(request, "core/home.html", {"editions": editions, "areas": areas})

def about(request):
    milestones = [
        ("2021", "Primeira edição piloto com 3 áreas de engenharia."),
        ("2022", "Expansão para 5 áreas e primeiros parceiros industriais."),
        ("2023", "Lançamento do portal de candidaturas online."),
        ("2024", "Mais de 180 alunos participantes ao longo do programa."),
    ]
    return render(request, "core/about.html", {"milestones": milestones})


def contact(request):
    return render(request, "core/contact.html")
