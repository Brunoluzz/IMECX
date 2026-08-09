from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

from core.storage import private_storage, cv_upload_path

def validate_file_size(value):

    #definir o tamanho
    limit_mb = 10

    if value.size > limit_mb * 1024 * 1024:
        raise ValidationError(
            f"Ficheiro demasiado grande. Máximo {limit_mb} MB."
        )

class EngineeringArea(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Área de Engenharia"
        verbose_name_plural = "Áreas de Engenharia"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Application(models.Model):
    STATUS = [
        ("pending", "Pendente"),
        ("review", "Em análise"),
        ("accepted", "Aceite"),
        ("rejected", "Rejeitada"),
    ]

    edition = models.ForeignKey("editions.Edition", on_delete=models.CASCADE, related_name="applications")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="applications")
    full_name = models.CharField(max_length=160)
    email = models.EmailField()
    university = models.CharField(max_length=160)
    course_year = models.PositiveSmallIntegerField()
    area = models.ForeignKey(EngineeringArea, on_delete=models.PROTECT)
    motivation = models.TextField()
    cv = models.FileField(
        upload_to=cv_upload_path,
        storage=private_storage,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["pdf"]
            ),
            validate_file_size,
        ],
        blank=True,
        null=True)
    status = models.CharField(max_length=20, choices=STATUS, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Candidatura"
        verbose_name_plural = "Candidaturas"

    def __str__(self):
        return f"{self.full_name} — {self.edition.year}"
    
    def create_participation(self):

        User = get_user_model()

        parts = self.full_name.split()

        first_name = parts[0] if parts else ""
        last_name = " ".join(parts[1:]) if len(parts) > 1 else ""

        user, created = User.objects.get_or_create(
            email=self.email,
            defaults={
                "username": self.email,
                "first_name": first_name,
                "last_name": last_name,
            }
        )

        if created:

            from allauth.account.models import EmailAddress

            email_address, email_created = EmailAddress.objects.get_or_create(
                user=user,
                email=user.email,
                defaults={
                    "verified": True,
                    "primary": True,
                }
            )

            if not email_created:
                email_address.verified = True
                email_address.primary = True
                email_address.save(
                    update_fields=[
                        "verified",
                        "primary",
                    ]
                )

        participation, created_participation = Participation.objects.get_or_create(
            user=user,
            edition=self.edition,
            defaults={
                "application": self,
                "status": "active",
                # Se a edicao ja estiver "A decorrer" quando a
                # candidatura e aceite, o participante entra logo
                # com os pontos iniciais em vez de esperar por uma
                # transicao de estado que ja aconteceu no passado.
                "points_baseline": (
                    self.edition.initial_points
                    if self.edition.status == "active"
                    else None
                ),
            }
        )

        if not participation.application:
            participation.application = self
            participation.save(update_fields=["application"])

        from applications.utils import send_account_activation_email

        if created:
            send_account_activation_email(
                user=user,
                edition=self.edition
            )

        if not self.user:
            self.user = user
            self.save(update_fields=["user"])

        return participation
    
    def save(self, *args, **kwargs):

        old_status = None

        if self.pk:
            old_status = (
                Application.objects
                .filter(pk=self.pk)
                .values_list("status", flat=True)
                .first()
            )

        super().save(*args, **kwargs)

        if self.status == "accepted" and old_status != "accepted":
            self.create_participation()
    

class Participation(models.Model):
    STATUS = [
        ("active", "Ativo"),
        ("withdrawn", "Desistiu"),
        ("removed", "Removido"),
        ("completed", "Concluiu"),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="active"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="participations"
    )

    edition = models.ForeignKey(
        "editions.Edition",
        on_delete=models.CASCADE,
        related_name="participations"
    )

    application = models.OneToOneField(
        "applications.Application",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    points_baseline = models.PositiveIntegerField(
        "Pontos iniciais",
        null=True,
        blank=True,
        help_text=(
            "Pontos com que o participante comecou a edicao. Fica "
            "vazio ate a edicao passar a 'A decorrer'. A pontuacao "
            "atual e calculada a partir daqui e das notas das tasks."
        ),
    )

    accepted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "edition")
        verbose_name = "Participação"
        verbose_name_plural = "Participações"

    @classmethod
    def get_for_user_and_edition(cls, user, edition):
        return cls.objects.filter(
            user=user,
            edition=edition
        ).first()
    
    @property
    def is_current(self):
        return (
            self.status == "active"
            and self.edition.status == "active"
        )


    @property
    def is_past(self):
        return self.edition.status == "finished"

    @property
    def current_points(self):
        """
        Pontuacao atual do participante nesta edicao, ou None se
        ainda nao foram atribuidos pontos iniciais (edicao ainda nao
        esta "A decorrer"). Cada task avaliada faz perder
        (task.points_value - nota) pontos; tasks sem submissao ou
        sem nota atribuida nao penalizam. Nunca desce abaixo de 0.
        """

        if self.points_baseline is None:
            return None

        lost = sum(
            submission.task.points_value - submission.grade
            for submission in self.submissions.select_related("task")
            if submission.grade is not None
        )

        return max(0, self.points_baseline - lost)

    @property
    def has_zero_points(self):
        return self.points_baseline is not None and self.current_points == 0

    def __str__(self):
        return f"{self.user.email} - {self.edition.year}"
