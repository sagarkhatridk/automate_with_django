import csv
from django.core.management.base import BaseCommand, CommandParser
import datetime
from django.apps import apps


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
            except LookupError as Error:
                self.stderr.write(self.style.ERROR(Error))

        if not model:
            self.stderr.write(f"Model '{model_name}' not found!.")
            return

        data = model.objects.all()

        # define the csv file name/path
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        file_path = f"exported_{model_name}_data_{timestamp}.csv"

        # open the CSV file and write the data.
        with open(file_path, 'w', newline="") as file:
            writer = csv.writer(file)

            # write the CSV header
            writer.writerow([field.name for field in model._meta.fields])

            # write data rows
            for row in data:
                writer.writerow([getattr(row, field.name) for field in model._meta.fields])

        self.stdout.write(self.style.SUCCESS("Data Exported Successfully."))