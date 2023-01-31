from django.contrib import admin
from tickets.models import AtendeeUser, Location, TicketType, Event, Booking, BookingDetail, BillingInfo, Payment, Ticket, Feedback, ContactNumber, ContactForm

# Register your models here.
admin.site.site_header = 'Etickets Admin Panel'

@admin.register(AtendeeUser)
class AtendeeUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'phone')
    search_fields = ('username', 'email')
    list_per_page = 10
    
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'place')
    search_fields =('created_at', 'updated_at')
    list_per_page = 10

@admin.register(TicketType)
class TicketType(admin.ModelAdmin):
    list_display = ('name', 'price')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_type', 'nos', 'start_time', 'end_time')
    list_per_page = 10

    def get_class_type(self, obj):
        return "\n".join([c.name for c in obj.class_type.all()])

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'booking_date', 'booking_time', 'status', 'event_dt')
   # list_filter = ('status')
    list_per_page = 10 
  
@admin.register(BookingDetail)
class BookingDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'event', 'place', 'event_date', 'start_time', 'end_time', 'noa', 'adult', 'child', 'ticket_type', 'ppa', 'total_price')
    list_filter = ('ticket_type', 'event')
    list_per_page = 10


@admin.register(BillingInfo)
class BillingInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'email', 'phone')
    list_per_page = 10


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'pay_amount', 'pay_method', 'phone', 'trxid', 'status')
    list_per_page = 10


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone', 'location', 'place', 'event_date', 'ticket_type', 'price')
    list_per_page = 10
    list_filter = ('place', 'ticket_type')

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'feedback')
    list_per_page = 10


@admin.register(ContactNumber)
class ContactNumberAdmin(admin.ModelAdmin):
    list_dispaly = ('location', 'location_phone', 'emergency_center', 'help_desk')
    list_per_page = 10


@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message')
    list_per_page = 10