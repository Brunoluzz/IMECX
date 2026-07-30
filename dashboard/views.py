from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from applications.models import Application
from editions.models import Edition


@staff_member_required
def index(request):
    stats = {
        "applications": Application.objects.count(),
        "pending": Application.objects.filter(status="pending").count(),
        "editions": Edition.objects.count(),
    }
    return render(request, "dashboard/index.html", {"stats": stats})
