from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from .models import Contact
from .forms import ContactForm
import requests


class ContactView(TemplateView):
    template_name = 'home.html'

    def get(self, request):
        form = ContactForm()

        return render(request, self.template_name, {'contact_form': form})

    def post(self, request):
        contact = Contact()
        contact.firstname = request.POST.get('firstname')
        contact.lastname = request.POST.get('lastname')
        contact.email = request.POST.get('email')
        r = requests.get('https://api.ipify.org?format=json')
        data = r.json()
        contact.ip = data['ip']
        contact.save()

        form = ContactForm(data=request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse('thankyou'))
        else:
            return render(request, self.template_name, {'contact_form': form})


class ThankyouView(TemplateView):
    template_name = 'thankyou.html'

    def get(self, request):
        contact = Contact.objects.latest('id')
        r = requests.get('https://api.ipify.org?format=json')
        data = r.json()
        return render(request, self.template_name, {'firstname': contact.firstname,'lastname': contact.lastname,'email': contact.email, 'ip': data['ip']})
