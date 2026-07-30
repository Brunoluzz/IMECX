from django.db import models


class Edition(models.Model):
    STATUS = [
        ("upcoming", "A anunciar"),
        ("open", "Candidaturas abertas"),
        ("closed", "Candidaturas fechadas"),
        ("full", "Vagas preenchidas totalmente"),
        ("active", "A decorrer"),
        ("finished", "Concluída"),
    ]

    year = models.IntegerField(unique=True)
    theme = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS, default="upcoming")
    applications_open = models.DateField(null=True, blank=True)
    applications_close = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-year"]
        verbose_name = "Edição"
        verbose_name_plural = "Edições"

    def __str__(self):
        return f"Imecx {self.year} — {self.theme}"

    @property
    def is_open(self):
        return self.status == "open"
    
    def save(self, *args, **kwargs):

        old_status = None

        if self.pk:
            old_status = (
                Edition.objects
                .filter(pk=self.pk)
                .values_list("status", flat=True)
                .first()
            )

        super().save(*args, **kwargs)

        if self.status == "finished" and old_status != "finished":

            from applications.models import Participation

            Participation.objects.filter(
                edition=self,
                status="active"
            ).update(
                status="completed"
            )
