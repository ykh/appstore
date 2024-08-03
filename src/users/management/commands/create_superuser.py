import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create the first superuser using environment variables.'

    def handle(self, *args, **kwargs):
        email = os.environ['INITIAL_ADMIN_EMAIL']
        password = os.environ['INITIAL_ADMIN_PASSWORD']

        user_model = get_user_model()

        if user_model.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING('Superuser already exists.'))
        else:
            user_model.objects.create_superuser(
                email=email,
                password=password,
            )
            self.stdout.write(self.style.SUCCESS('Superuser created successfully.'))
