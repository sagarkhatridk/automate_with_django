import hashlib
from django.apps import apps
from django.core.management.base import CommandError
import csv
from django.db import DataError
from django.core.mail import EmailMessage
from django.conf import settings
import datetime
import os
import time
from emails.models import Email, Sent, EmailTracking, Subscriber
from bs4 import BeautifulSoup

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

def send_email_notification(mail_subject, message, to_email, attechment=None, email_id=None):
    try:
        from_email = settings.DEFAULT_FROM_EMAIL
        for recipient_email in to_email:
            # create email tracking record
            new_message = message
            if email_id:
                email = Email.objects.get(pk=email_id)
                subscriber = Subscriber.objects.get(email_list=email.email_list, email_address=recipient_email)
                timestamp = str(time.time())
                data_to_hash = f"{recipient_email}{timestamp}"
                unique_id = hashlib.sha256(data_to_hash.encode()).hexdigest()
                email_tracking = EmailTracking.objects.create(
                    email=email,
                    subscriber=subscriber,
                    unique_id=unique_id
                )

                # generate the tracking pixel url
                base_url = settings.BASE_URL
                click_tracking_url = f"{base_url}/emails/track/click/{unique_id}"
                open_tracking_url = f"{base_url}/emails/track/open/{unique_id}"

                # search for the linkns in the email body
                soup = BeautifulSoup(message, 'html.parser')
                urls = [a['href'] for a in soup.find_all('a', href=True)]

                # if there are links or urls in the email body, inject our click tracking url to that link

                if urls:
                    for url in urls:
                        # make the final tracking url.
                        tracking_url = f"{click_tracking_url}?url={url}"
                        new_message = new_message.replace(f"{url}", f"{tracking_url}")
                else:
                    print("No URL(s) Found in email Content.")

                #  create the email content with tracking pixel image
                open_tracking_img = f"<img src='{open_tracking_url}' width='1' height='1'>"
                new_message = new_message + open_tracking_img

            mail = EmailMessage(mail_subject, new_message, from_email, to=[recipient_email])
            if attechment is not None:
                mail.attach_file(attechment)
            mail.content_subtype = "html"
            mail.send()

        # store the total sent emails inside the Sent Model
        if email_id:
            sent = Sent()
            sent.email = email
            sent.total_sent = email.email_list.count_emails()
            sent.save()

    except Exception as E:
        raise E


def generate_csv_file(model_name):
    # define the csv file name/path
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    export_dir = 'exported_data'

    file_name = f"exported_{model_name}_data_{timestamp}.csv"
    file_path = os.path.join(settings.MEDIA_ROOT, export_dir, file_name)
    return file_path