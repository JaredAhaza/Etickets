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


class BookingDetail(models.Model):
    booking = models.OneToOneField(Booking, null=True, blank=True, on_delete=models.CASCADE)
    event = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    place = models.CharField(max_length=255, null=True, blank=True)
    event_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    noa = models.PositiveIntegerField(verbose_name=_("Number of atendees"), null=True, blank=True)
    adult = models.PositiveIntegerField(null=True, blank=True)
    child = models.PositiveIntegerField(null=True, blank=True)
    ticket_type = models.CharField(max_length=255, null=True, blank=True)
    ppa = models.PositiveIntegerField(verbose_name=_("price Per Atendee"), null=True, blank=True)
    total_fare = models.PositiveIntegerField(null=True, blank=True)

    event_dt = models.DateTimeField(blank=True, null=True)
    booking_dt = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

class BillingInfo(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(AtendeeUser, on_delete=models.PROTECT, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(AtendeeUser, on_delete=models.PROTECT, null=True, blank=True)
    pay_amount = models.PositiveIntegerField(null=True, blank=True)
    pay_method = models.CharField(max_length=25, null=True, blank=True)
    phone = models.CharField(max_length=14, null=True, blank=True)
    trxid = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Transaction Id"))
    status = models.CharField(max_length=50, default='Paid', auto_created=True, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class Ticket(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(AtendeeUser, on_delete=models.PROTECT, null=True, blank=True)
    phone = models.CharField(max_length=13, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    place = models.CharField(max_length=255, null=True, blank=True)
    event_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    event_name = models.CharField(max_length=255, null=True, blank=True)
    start_time = models.CharField(max_length=255, null=True, blank=True)
    price = models.PositiveIntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class Feedback(models.Model):
    name = models.CharField(verbose_name=_("user name"), max_length=255, null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

class ContactNumber(models.Model):
    location = models.OneToOneField(Location, on_delete=models.CASCADE, null=True, blank=True)
    location_phone = models.CharField(verbose_name=_("location Phone Number"), max_length=255, null=True, blank=True)
    emergency_center = models.CharField(verbose_name=_("Emergency Center Phone Number"), max_length=255, null=True, blank=True)
    help_desk = models.CharField(verbose_name=_("Help Desk Phone Number"), max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class ContactForm(models.Model):
    name = models.CharField(verbose_name=_("Sender Name"), max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True) 