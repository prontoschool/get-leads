from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse

# Create your views here.
class ContactView(TemplateView):
    template_name = 'home.html'
    def get(self, request):
        return render(request, self.template_name, {'name': 'intern'})
