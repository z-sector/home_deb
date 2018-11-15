from django.core.management.base import BaseCommand
from django.conf import settings

import getpass

from apps.user_management.accounts.models import User


class Command(BaseCommand):
    help = 'Utility to create a superuser'

    def handle(self, *args, **options):
        # User.objects.create_superuser()
        self.stdout.write(self.style.SUCCESS(self.help))

        username = None
        while username is None:
            username = input('Enter username: ').lower()
            if username == 'exit':
                return 'Bye-Bye!'
            if not settings.REG_USER_NAME.match(username):
                username = None
                self.stdout.write(self.style.NOTICE('Username does not match the pattern.'))
                self.stdout.write(self.style.WARNING('To logout type "exit"'))

        email = None
        while email is None:
            email = input('Enter email: ')
            if email == 'exit':
                return 'Bye-Bye!'
            if not settings.REG_EMAIL.match(email):
                email = None
                self.stdout.write(self.style.WARNING('Email does not match the pattern.'))
                self.stdout.write(self.style.NOTICE('To logout type "exit"'))

        password_1 = None
        while password_1 is None:
            password_1 = getpass.getpass()
            if password_1 == 'exit':
                return 'Bye-Bye!'
            if not settings.REG_PASSWORD.match(password_1):
                password_1 = None
                self.stdout.write(self.style.WARNING('Password does not match the pattern. '
                                                     'Must be at least 12 characters, '
                                                     'two lowercase and uppercase letters, '
                                                     'two number and one special character (example, ! @ # $% ^ & *)'))
                self.stdout.write(self.style.NOTICE('To logout type "exit"'))

            password_2 = None
            while password_2 is None and password_1:
                password_2 = getpass.getpass('Password (again): ')
                if password_2 == 'exit':
                    return 'Bye-Bye!'
                if password_1 != password_2:
                    password_1 = None
                    password_2 = None
                    self.stdout.write(self.style.WARNING('Passwords do not mach'))
                    self.stdout.write(self.style.NOTICE('To logout type "exit"'))

        User.objects.create_superuser(username, email, password_1)

        print(username)



        # email = input('email')
        # print(email)
        # password_1 = getpass.getpass()
        # password_2 = getpass.getpass('Password (again): ')
