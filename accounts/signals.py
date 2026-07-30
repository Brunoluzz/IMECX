import hashlib

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile

AVATAR_PALETTE = [
    "#E63946", "#F4A261", "#2A9D8F", "#264653",
    "#E76F51", "#457B9D", "#8E44AD", "#D62828",
    "#1D3557", "#2B9348", "#BC6C25", "#6A4C93",
]


def pick_avatar_color(seed: str) -> str:
    digest = hashlib.md5(seed.encode("utf-8")).hexdigest()
    index = int(digest, 16) % len(AVATAR_PALETTE)
    return AVATAR_PALETTE[index]


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_on_user_creation(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(
            user=instance,
            defaults={"avatar_color": pick_avatar_color(instance.username or instance.email)},
        )