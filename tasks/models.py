from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

from core.storage import private_storage, task_submission_upload_path

def validate_file_size(value):

    #definir o tamanho
    limit_mb = 20

    if value.size > limit_mb * 1024 * 1024:
        raise ValidationError(
            f"Ficheiro demasiado grande. Máximo {limit_mb} MB."
        )

# Create your models here.
class Task(models.Model):

    edition = models.ForeignKey(
        "editions.Edition",
        on_delete=models.CASCADE,
        related_name="tasks"
    )

    title = models.CharField(max_length=200)

    description = models.TextField()

    assigned_participants = models.ManyToManyField(
        "applications.Participation",
        related_name="tasks"
    )

    deadline = models.DateTimeField(
        null=True,
        blank=True
    )

    points_value = models.PositiveIntegerField(
        "Pontos da task",
        default=10,
        help_text=(
            "Quanto vale esta task. Um participante que receba a "
            "nota maxima nao perde pontos; nota 0 faz perder estes "
            "pontos todos."
        ),
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.title

class TaskSubmission(models.Model):

    STATUS = [
        ("submitted", "Submetida"),
        ("revision", "Necessita revisão"),
        ("approved", "Aprovada"),
        ("rejected", "Rejeitada"),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="submitted"
    )

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="submissions"
    )

    participant = models.ForeignKey(
        "applications.Participation",
        on_delete=models.CASCADE,
        related_name="submissions"
    )

    #verificar as extensoes pretendidas
    file = models.FileField(
        upload_to=task_submission_upload_path,
        storage=private_storage,
        validators=[
            FileExtensionValidator(
                allowed_extensions= [
                    "zip",
                    "pdf",
                ]
            ),
            validate_file_size,
        ]
    )

    comment = models.TextField(blank=True)

    submitted_at = models.DateTimeField(
        auto_now_add=True
    )

    admin_feedback = models.TextField(blank=True)

    grade = models.PositiveIntegerField(
        "Nota",
        null=True,
        blank=True,
        help_text="Nota de 0 ate ao valor da task. Deixar vazio enquanto nao for avaliada.",
    )

    class Meta:
        unique_together = (
            "task",
            "participant"
        )

    def clean(self):
        super().clean()

        if self.grade is not None and self.task_id and self.grade > self.task.points_value:
            raise ValidationError({
                "grade": (
                    f"A nota nao pode ser maior do que o valor da "
                    f"task ({self.task.points_value} pontos)."
                )
            })

    def __str__(self):
        return f"{self.participant.user.email} - {self.task.title}"
    
class Notification(models.Model):

    TYPE = [
        ("task_assigned", "Task atribuída"),
        ("task_feedback", "Feedback da task"),
        ("general", "Geral"),
    ]

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    title = models.CharField(
        max_length=200
    )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    type = models.CharField(
        max_length=20,
        choices=TYPE,
        default="general",
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.recipient.email} - {self.title}"