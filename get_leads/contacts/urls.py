from django.conf.urls import url

from .views import ContactView, ThankyouView

urlpatterns = [
    url(r'^$', ContactView.as_view()),
    url(r'^thankyou/$', ThankyouView.as_view()),
]
