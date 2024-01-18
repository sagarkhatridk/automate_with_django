from django.core.management.base import BaseCommand, CommandError
from django.db import DataError
from dataentry.models import Student
import csv
from django.apps import apps

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

        # Search for model across all installed apps.
        model = None
        for app_config in apps.get_app_configs():
            # Try to search for the model.
            try:
                model = apps.get_model(app_label=app_config.label, model_name=model_name)
                break # stop searching once model is found
            except LookupError:
                continue # model not found in this app \
                            #continue searcing for the next app.

        if not model:
            raise CommandError(f"Model '{model_name}' not found in any App.")

        # compare csv header with model's field names
        #  get all the field names of the modal that we found
        model_fields = [field.name for field in model._meta.fields if field.name != 'id']

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            csv_header = reader.fieldnames

            # compare the csv header to the model fields
            if csv_header != model_fields:
                raise DataError(f"CSV file does't match the {model_name} table fields.")

            for row in reader:
                model.objects.create(**row)


        self.stdout.write(self.style.SUCCESS("Data inserted Successfully"))