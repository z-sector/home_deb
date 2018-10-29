from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse


# Create your views here.

class ChangeView(View):
    template_name = 'change.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
