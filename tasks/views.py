from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Task, TaskSubmission, Notification
from django.core.exceptions import PermissionDenied
from applications.models import Participation
from .forms import TaskSubmissionForm
from django.views.decorators.http import require_POST
from django.http import JsonResponse

@login_required
def my_tasks(request):

    participation = get_object_or_404(
        Participation,
        user=request.user,
        status="active",
        edition__status="active"
    )

    tasks = (
        participation.tasks
        .all()
        .prefetch_related("submissions")
    )

    pending_count = 0
    revision_count = 0
    approved_count = 0

    active_tasks = []
    archived_tasks = []

    for task in tasks:

        submission = TaskSubmission.objects.filter(
            task=task,
            participant=participation
        ).first()

        task.submission = submission

        if not submission:
            pending_count += 1

        elif submission.status == "revision":
            revision_count += 1

        elif submission.status == "approved":
            approved_count += 1

        if task.is_active:
            active_tasks.append(task)
        else:
            archived_tasks.append(task)

    return render(
        request,
        "tasks/my_tasks.html",
        {
            "participation": participation,
            "active_tasks": active_tasks,
            "archived_tasks": archived_tasks,
            "pending_count": pending_count,
            "revision_count": revision_count,
            "approved_count": approved_count,
        }
    )

@login_required
def submit_task(request, task_id):

    task = get_object_or_404(
        Task,
        pk=task_id
    )

    participation = get_object_or_404(
        Participation,
        user=request.user,
        edition=task.edition,
        status="active"
    )

    if task.edition.status != "active":
        raise PermissionDenied

    if not task.assigned_participants.filter(
        pk=participation.pk
    ).exists():
        raise PermissionDenied

    existing_submission = TaskSubmission.objects.filter(
        task=task,
        participant=participation
    ).first()

    if request.method == "POST":

        if not task.is_active:
            raise PermissionDenied

        form = TaskSubmissionForm(
            request.POST,
            request.FILES,
            instance=existing_submission,
        )

        if form.is_valid():

            submission = form.save(commit=False)

            submission.task = task
            submission.participant = participation
            submission.is_missing = False
            submission.grade = None

            submission.save()

            Notification.objects.filter(
                recipient=request.user,
                task=task,
                type__in=["task_assigned", "task_feedback"],
                is_read=False
            ).update(
                is_read=True
            )

            return redirect(
                "tasks:my_tasks",
            )

    else:

        form = TaskSubmissionForm(
            instance=existing_submission,
            disabled=not task.is_active,
        )

    return render(
        request,
        "tasks/submit_tasks.html",
        {
            "task": task,
            "form": form,
            "submission": existing_submission,
        }
    )

@login_required
def task_detail(request, task_id):

    task = get_object_or_404(
        Task,
        pk=task_id
    )

    participation = get_object_or_404(
        Participation,
        user=request.user,
        edition=task.edition,
        status="active"
    )

    if task.edition.status != "active":
        raise PermissionDenied    

    if not task.assigned_participants.filter(
        pk=participation.pk
    ).exists():
        raise PermissionDenied

    submission = TaskSubmission.objects.filter(
        task=task,
        participant=participation
    ).first()

    return render(
        request,
        "tasks/task_detail.html",
        {
            "task": task,
            "submission": submission,
        }
    )

@login_required
@require_POST
def mark_notification_read(request, pk):

    notification = get_object_or_404(
        Notification,
        pk=pk,
        recipient=request.user,
    )

    notification.is_read = True
    notification.save()

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"ok": True})

    return redirect(
        request.META.get("HTTP_REFERER", "/")
    )


@login_required
@require_POST
def mark_all_notifications_read(request):

    request.user.notifications.filter(
        is_read=False
    ).update(
        is_read=True
    )

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"ok": True})

    return redirect(
        request.META.get("HTTP_REFERER", "/")
    )