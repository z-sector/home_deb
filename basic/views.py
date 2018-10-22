from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse


# Create your views here.


class MainView(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class AboutView(View):
    template_name = 'about.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class ContactView(View):
    template_name = 'contact.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class FaqView(View):
    template_name = 'faq.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
