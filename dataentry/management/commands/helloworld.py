"""
Command for Pringtin Hello world
"""
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Prints Hello World!."

    def handle(self, *args, **options):
        """command logic will go here"""
        self.stdout.write('Hello World!.')