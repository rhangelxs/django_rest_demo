from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


class Location(models.Model):
    country = models.CharField(_("Country name"), blank=True, max_length=255)
    city = models.CharField(_("City name"), blank=True, max_length=255)
    description = models.TextField(_("Description"), blank=True)

    def get_absolute_url(self):
        return reverse("locations:detail", kwargs={"id": self.pk})


class Visit(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    date = models.DateTimeField(_("Date"), default=now)
    ratio = models.IntegerField(_("Raiting"), validators=[MinValueValidator(0), MaxValueValidator(10)])

    def get_absolute_url(self):
        return reverse("locations:detail", kwargs={"id": self.pk})
