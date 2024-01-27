from django.core.management.base import BaseCommand, CommandError
from dataentry.utils import check_csv_function
import csv
class Command(BaseCommand):
    """python manage.py insertdata {{file path}} {{model_name}}"""

    help = "import data from CSV file"

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help="Path to the CSV file.")
        parser.add_argument("model_name", type=str, help="Name of the Model.")

    def handle(self, *args, **kwargs):
        """logic of import data from CSV."""
        file_path = kwargs['file_path']
        model_name = kwargs['model_name'].capitalize()

        model = check_csv_function(file_path, model_name)
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                model.objects.create(**row)


        self.stdout.write(self.style.SUCCESS("Data inserted Successfully"))