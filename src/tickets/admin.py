from django.contrib import admin
from apps.models import AtendeeUser

# Register your models here.
admin.site.site_header = 'LTTP Admin Panel'


@admin.register(AtendeeUser)
class AtendeeUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'phone')
    search_fields = ('username', 'email')
    list_per_page = 10

