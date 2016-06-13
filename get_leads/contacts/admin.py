from django.contrib import admin

from .models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_display = ('firstname','lastname','email')
admin.site.register(Contact, ContactAdmin)
