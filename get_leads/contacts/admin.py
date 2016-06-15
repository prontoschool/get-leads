from django.contrib import admin

from .models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_filter = ('name','ip','email','country')
    search_fields = ['ip','email','country']
    list_display = ('name','email','ip','country')

admin.site.register(Contact, ContactAdmin)
