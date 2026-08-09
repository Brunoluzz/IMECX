import uuid
from pathlib import Path

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.urls import reverse


class PrivateMediaStorage(FileSystemStorage):
    """
    Storage para ficheiros sensiveis (CVs, submissoes de tasks).

    Ao contrario do storage por omissao, os ficheiros ficam fora da
    pasta publica MEDIA_ROOT e nunca sao acessiveis diretamente por
    URL. O metodo url() aponta sempre para a view autenticada
    'core:secure_media', que valida se quem pede o ficheiro e o
    dono ou um membro da equipa (staff) antes de o servir.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("location", settings.PRIVATE_MEDIA_ROOT)
        kwargs.setdefault("base_url", None)
        super().__init__(*args, **kwargs)

    def url(self, name):
        return reverse("core:secure_media", kwargs={"path": name})


private_storage = PrivateMediaStorage()


def _random_name(prefix, filename):
    ext = Path(filename).suffix.lower()
    return f"{prefix}/{uuid.uuid4().hex}{ext}"


# Funcoes 'upload_to' de nivel de modulo (nao closures): as
# migrations do Django guardam uma referencia importavel para a
# funcao, por isso tem de ser possivel importa-la pelo caminho
# "core.storage.<nome>".

def cv_upload_path(instance, filename):
    """Nome aleatorio para CVs de candidaturas, mantendo a extensao."""
    return _random_name("cvs", filename)


def task_submission_upload_path(instance, filename):
    """Nome aleatorio para submissoes de tasks, mantendo a extensao."""
    return _random_name("task_submissions", filename)
