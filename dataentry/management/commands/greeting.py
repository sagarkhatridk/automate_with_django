"""
Command for greeting
"""
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """Proposed command: python manage.py greeting {{name}}."""
    """Proposed output: Hi {{name}}."""

    help = "Greets the User."

    def add_arguments(self, parser):
        """will takecare of arguments to the command."""
        parser.add_argument('name', type=str, help='Specifies username.')

    def handle(self, *args, **kwargs):
        """command logic will go here"""
        name = kwargs['name']
        greeting = f'Hi {name}, Good Morning!.'
        return self.stdout.write(self.style.SUCCESS(greeting))
