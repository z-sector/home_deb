from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from accounts.models import User


# Create your views here.


class MainView(View):
    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class ConsumersView(View):
    template_name = 'register_consumers.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class OrganizationsView(View):
    template_name = 'register_organizations.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class RegulatorsView(View):
    template_name = 'register_regulators.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class RegistrationView(View):
    template_name = 'test.html'

    def post(self, request, *args, **kwargs):
        errors = {}
        data = {key: ''.join(value) for key, value in request.POST.items()}
        token = data.pop('csrfmiddlewaretoken')
        password = data.pop('password')
        user = User(**data)
        user.set_password(password)
        try:
            user.validate_unique()
        except ValidationError as er:
            errors.update(er.message_dict)
        if errors:
            print('!!!!!!!!!!!!!!!!!!!!!!!!')
            return render(request, 'test.html', {'reg_errors': errors, 'username': data.get('email')})
        user.save()

        return render(request, 'test.html', {'username': data.get('email')})


