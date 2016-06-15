from django.contrib import admin

from .models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_filter = ('name', 'ip', 'email')
    search_fields = ['ip','email']
    list_display = ('name','email','ip')

admin.site.register(Contact, ContactAdmin)
