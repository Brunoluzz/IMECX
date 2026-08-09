from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from applications.models import Application, Participation
from editions.models import Edition


@staff_member_required
def index(request):
    zero_points = [
        p for p in Participation.objects.filter(
            status="active",
            points_baseline__isnull=False,
        ).select_related("user", "edition")
        if p.current_points == 0
    ]

    stats = {
        "applications": Application.objects.count(),
        "pending": Application.objects.filter(status="pending").count(),
        "editions": Edition.objects.count(),
        "zero_points_count": len(zero_points),
    }
    return render(request, "dashboard/index.html", {
        "stats": stats,
        "zero_points": zero_points,
    })
