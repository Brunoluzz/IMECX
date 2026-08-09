from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import FileResponse, Http404
from django.shortcuts import render
from django.contrib import messages
from editions.models import Edition
from applications.models import EngineeringArea

from .storage import private_storage


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


@login_required
def secure_media(request, path):
    """
    Serve ficheiros privados (CVs de candidaturas, submissoes de
    tasks) apenas ao respetivo dono ou a membros da equipa (staff).
    Qualquer outro utilizador autenticado recebe 403; um pedido
    para um caminho que nao pertence a nenhum registo conhecido
    recebe 404 (nao revela se o ficheiro existe ou nao).
    """

    from applications.models import Application
    from tasks.models import TaskSubmission

    owner = None

    application = Application.objects.filter(cv=path).select_related("user").first()

    if application:
        owner = application.user
    else:
        submission = (
            TaskSubmission.objects
            .filter(file=path)
            .select_related("participant__user")
            .first()
        )
        if submission:
            owner = submission.participant.user

    if owner is None:
        raise Http404

    is_owner = owner.pk == request.user.pk

    if not (request.user.is_staff or is_owner):
        raise PermissionDenied

    if not private_storage.exists(path):
        raise Http404

    return FileResponse(
        private_storage.open(path, "rb"),
        as_attachment=True,
        filename=path.rsplit("/", 1)[-1],
    )
