import csv
from django.core.management.base import BaseCommand
import datetime
from django.apps import apps
from dataentry.utils import generate_csv_file

class Command(BaseCommand):
    """python manage.py exportdata {{model_name}}"""

    help = "Export data from Student model to CSV file."

    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str, help="Model Name")


    def handle(self, *args, **kwargs):
        # fetch the data from the databse
        model_name = kwargs['model_name'].capitalize()

        # search through all the installed apps for the model.
        model = None
        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(app_label=app_config.label, model_name=model_name)
                break # stop search if model found
            except LookupError:
                pass

        if not model:
            self.stderr.write(f"Model '{model_name}' not found!.")
            return

        data = model.objects.all()


        # generate CSV file_path
        file_path = generate_csv_file(model_name)

        # open the CSV file and write the data.
        with open(file_path, 'w', newline="") as file:
            writer = csv.writer(file)

            # write the CSV header
            writer.writerow([field.name for field in model._meta.fields])

            # write data rows
            for row in data:
                writer.writerow([getattr(row, field.name) for field in model._meta.fields])

        self.stdout.write(self.style.SUCCESS("Data Exported Successfully."))