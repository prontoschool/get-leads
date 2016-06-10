from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from .models import Contact


class ContactView(TemplateView):
    template_name = 'home.html'

    def get(self, request):
        return render(request, self.template_name, {'name': 'intern'})

    def post(self, request):
        contact = Contact()
        contact.firstname = request.POST.get('firstname')
        contact.lastname = request.POST.get('lastname')
        contact.save()
        return HttpResponseRedirect(reverse('thankyou'))


class ThankyouView(TemplateView):
    template_name = 'thankyou.html'

    def get(self, request):
        return render(request, self.template_name)
