from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse


class ContactView(TemplateView):
    template_name = 'home.html'

    def get(self, request):
        return render(request, self.template_name, {'name': 'intern'})


class ThankyouView(TemplateView):
    template_name = 'thankyou.html'

    def get(self, request):
        return render(request, self.template_name)
