# accounts/models.py
from django.conf import settings
from django.db import models

class Profile(models.Model):

    class Role(models.TextChoices):
        FUNCIONARIO = "funcionario", "Funcionário"
        TECNICO = "tecnico", "Técnico"
        ADMIN = "admin", "Administrador"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    phone = models.CharField("Telefone", max_length=20, blank=True)
    bio = models.TextField("Sobre mim", blank=True)
    avatar_color = models.CharField(max_length=7, default="#457B9D")
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    role = models.CharField(
        "Cargo",
        max_length=20,
        choices=Role.choices,
        default=Role.FUNCIONARIO,
    )

    @property
    def initials(self) -> str:
        u = self.user

        first = (u.first_name or "").strip()
        last = (u.last_name or "").strip()

        if first:

            last_initial = ""

            if last:
                last_initial = last.split()[-1][:1]

            return (
                first[:1] + last_initial
            ).upper()

        base = (
            u.email
            or u.username
            or "?"
        ).strip()

        return base[:1].upper()
    
    def __str__(self):
        return f"Perfil de {self.user}"
