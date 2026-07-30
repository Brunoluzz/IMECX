from django.contrib import admin
from .models import Notification, Task, TaskSubmission

# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "edition",
        "deadline",
        "is_active",
        "submission_count",
    )

    list_filter = (
        "edition",
        "is_active",
    )

    search_fields = (
        "title",
        "description",
    )

    filter_horizontal = (
        "assigned_participants",
    )

    def submission_count(self, obj):
        return obj.submissions.count()

    submission_count.short_description = "Submissões"

    def save_related(self, request, form, formsets, change):

        super().save_related(
            request,
            form,
            formsets,
            change
        )

        task = form.instance

        for participation in task.assigned_participants.all():

            already_notified = Notification.objects.filter(
                recipient=participation.user,
                task=task,
                type="task_assigned",
            ).exists()

            if not already_notified:

                Notification.objects.create(
                    recipient=participation.user,
                    task=task,
                    type="task_assigned",
                    title="Nova tarefa atribuída",
                    message=(
                        f"Foi-te atribuída a tarefa "
                        f"'{task.title}'."
                    ),
                )

@admin.register(TaskSubmission)
class TaskSubmissionAdmin(admin.ModelAdmin):

    list_display = (
        "task",
        "participant",
        "status",
        "submitted_at",
    )

    list_filter = (
        "task",
        "status",
        "task__edition",
    )

    search_fields = (
        "participant__user__email",
        "participant__user__first_name",
        "participant__user__last_name",
        "task__title",
    )

    fields = (
        "task",
        "participant",
        "file",
        "comment",
        "status",
        "admin_feedback",
    )

    def save_model(self, request, obj, form, change):

        old_status = None
        old_feedback = None

        if change:

            previous = TaskSubmission.objects.get(
                pk=obj.pk
            )

            old_status = previous.status
            old_feedback = previous.admin_feedback

        super().save_model(
            request,
            obj,
            form,
            change
        )

        if (
            change and (
                old_status != obj.status
                or old_feedback != obj.admin_feedback
            )
        ):

            Notification.objects.create(
                recipient=obj.participant.user,
                task=obj.task,
                type="task_feedback",
                title=f"Atualização da task: {obj.task.title}",
                message=(
                    obj.admin_feedback
                    or f"Estado alterado para {obj.get_status_display()}."
                ),
            )