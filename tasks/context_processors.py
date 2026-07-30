from applications.models import Participation

def notifications_context(request):

    if not request.user.is_authenticated:
        return {
            "unread_notifications": 0,
            "latest_notifications": [],
            "active_participation": None,
        }

    notifications = (
        request.user.notifications
        .filter(is_read=False)
        .select_related("task")
    )

    active_participation = (
        Participation.objects
        .filter(
            user=request.user,
            status="active",
            edition__status="active",
        )
        .select_related("edition")
        .first()
    )

    return {
        "unread_notifications": notifications.count(),
        "latest_notifications": notifications[:5],
        "active_participation": active_participation,
    }