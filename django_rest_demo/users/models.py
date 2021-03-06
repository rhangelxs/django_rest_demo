from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, IntegerField, DateField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = CharField(_("Name of User"), blank=True, max_length=255)

    MALE = 1
    FEMALE = 2

    GENDERS = (
        (MALE, 'Man'),
        (FEMALE, 'Woman'),
    )

    gender = IntegerField(choices=GENDERS, blank=True, null=True)

    birth_date = DateField(blank=True, null=True)

    country = CharField(_("Country name"), blank=True, max_length=255)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
