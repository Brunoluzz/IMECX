from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Task, TaskSubmission, Notification
from django.core.exceptions import PermissionDenied
from applications.models import Participation
from .forms import TaskSubmissionForm

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

    return render(
        request,
        "tasks/my_tasks.html",
        {
            "participation": participation,
            "tasks": tasks,
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

        form = TaskSubmissionForm(
            request.POST,
            request.FILES,
            instance=existing_submission
        )

        if form.is_valid():

            submission = form.save(commit=False)

            submission.task = task
            submission.participant = participation

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
            instance=existing_submission
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
def mark_notification_read(request, pk):

    notification = get_object_or_404(
        Notification,
        pk=pk,
        recipient=request.user,
    )

    notification.is_read = True
    notification.save()

    return redirect(
        request.META.get("HTTP_REFERER", "/")
    )


@login_required
def mark_all_notifications_read(request):

    request.user.notifications.filter(
        is_read=False
    ).update(
        is_read=True
    )

    return redirect(
        request.META.get("HTTP_REFERER", "/")
    )