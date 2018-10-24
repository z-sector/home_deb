from django.views.generic.base import View
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import auth
import redis


# Create your views here.


# class MainView(View):
#     template_name = 'index.html'
#
#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name)


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
        r = redis.StrictRedis('redis', port=6379)
        # s = r.set("key1", "value1")
        # s = r.get("key1").decode('utf-8')
        # print(s)
        s = r.keys('*')
        print(s)

        return render(request, self.template_name)

class DashboardView(View):
    template_name = 'dashboard.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return render(request, "dashboard.html", {'username':username})
        else:
            return render(request, "error_login.html", {'error': True})

    return render(request, "index.html")
