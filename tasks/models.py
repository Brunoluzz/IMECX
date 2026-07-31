from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

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
        on_delete=models.CASCADE
    )

    #verificar as extensoes pretendidas
    file = models.FileField(
        upload_to="task_submissions/",
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

    class Meta:
        unique_together = (
            "task",
            "participant"
        )

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