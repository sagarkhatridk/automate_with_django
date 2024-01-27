from django.apps import apps
from django.core.management.base import CommandError
import csv
from django.db import DataError
from django.core.mail import EmailMessage
from django.conf import settings
import datetime
import os

def get_all_custom_models():
    default_models = [
        'ContentType', 'Session', 'LogEntry', 'Group', 'Permission', 'User', 'Upload'
    ]
    # try to get all the apps
    return [model.__name__ for model in apps.get_models() if model.__name__ not in default_models ]

def check_csv_function(file_path, model_name):
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

    #  get all the field names of the modal that we found
    model_fields = [field.name for field in model._meta.fields if field.name != 'id']

    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            csv_header = reader.fieldnames

            # compare the csv header to the model fields
            if csv_header != model_fields:
                raise DataError(f"CSV file does't match the {model_name} table fields.")
    except Exception as E:
        raise E

    return model

def send_email_notification(mail_subject, message, to_email, attechment=None):
    try:
        from_email = settings.DEFAULT_FROM_EMAIL
        mail = EmailMessage(mail_subject, message, from_email, to=[to_email])

        if attechment is not None:
            mail.attach_file(attechment)
        mail.send()
    except Exception as E:
        raise E


def generate_csv_file(model_name):
    # define the csv file name/path
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    export_dir = 'exported_data'

    file_name = f"exported_{model_name}_data_{timestamp}.csv"
    file_path = os.path.join(settings.MEDIA_ROOT, export_dir, file_name)
    return file_path