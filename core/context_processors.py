from editions.models import Edition


def site_context(request):
    current = (
        Edition.objects.filter(status__in=["open", "active", "upcoming"]).first()
        or Edition.objects.first()
    )
    return {
        "site_name": "Imecx",
        "current_edition": current,
    }
