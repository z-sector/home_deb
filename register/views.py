from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse


# Create your views here.


class MainView(View):
    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class ConsumersView(View):
    template_name = 'about.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class OrganizationsView(View):
    template_name = 'contact.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class Regulators(View):
    template_name = 'faq.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)