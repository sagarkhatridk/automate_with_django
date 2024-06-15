import os
import subprocess
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """python manage.py black"""

    help = "To apply black formatter in all views.py."

    def add_arguments(self, parser):
        parser.add_argument('directory', type=str, help="Directory Path")

    def handle(self, *args, **kwargs):

        directory = kwargs['directory']

        for root, dirs, files in os.walk(directory):
            for file in files:
                if file == 'views.py':
                    file_path = os.path.join(root, file)
                    subprocess.run(['black', file_path])

        self.stdout.write(self.style.SUCCESS("black formatter applied Successfully."))