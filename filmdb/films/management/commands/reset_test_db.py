from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Resets test database'

    def handle(self, *args, **options):
        call_command('reset_db', interactive=False)
        call_command('migrate')
        User.objects.create_superuser('test', password='test')
