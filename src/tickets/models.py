from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.
class AtendeeUser(AbstractUser):
    email = models.EmailField(max_length=100, blank=True, unique=True, null=True)
    phone = models.CharField(verbose_name=_("Mobile phone"), max_length=14, blank=True, null=True, unique=True)
    photo = models.ImageField(verbose_name=_("Photo"), upload_to='users/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.email}"


class Location(models.Model):
    name = models.CharField(verbose_name=_("Station Name"), max_length=255, null=True, blank=True)
    place = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.name}, {self.place}"


class TicketType(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    price = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(verbose_name=_("Event Name"), max_length=255, null=True, blank=True)
    nos = models.PositiveIntegerField(verbose_name=_("Number of Seat"), null=True, blank=True)
    event_type = models.ForeignKey(Location, null=True, blank=True, on_delete=models.PROTECT)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    ticket_type = models.ManyToManyField(TicketType, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    status = (
        ("Pending", "Pending"),
        ("Accepted", "Accepted"),
        ("Canceled", "Canceled"),
    )
    user = models.ForeignKey(AtendeeUser, null=True, blank=True, on_delete=models.PROTECT)
    booking_date = models.DateField(auto_now_add=True, null=True, blank=True)
    booking_time = models.TimeField(auto_now_add=True, null=True, blank=True)
    status = models.CharField(max_length=50, default='Pending', choices=status, auto_created=True, null=True, blank=True)
    event_date = models.DateField(null=True, blank=True)
    event_dt = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
