from awd_main.celery import app
import time
from django.core.management import call_command
from .utils import send_email_notification, generate_csv_file
from django.conf import settings

@app.task
def celery_test_task():
    time.sleep(5) # simulation of any task taht's going to take 5 seconds

    # send an email
    mail_subject = 'Test Subject'
    message = ' This is a test email'
    to_email = settings.DEFAULT_TO_EMAIL
    send_email_notification(mail_subject, message, to_email)
    return 'Task Exewcuted by celery Successfully'

@app.task
def import_data_task(file_path, model_name):
    try:
        call_command('importdata', file_path, model_name)
    except Exception as E:
        raise E

    # notify the user by email
    mail_subject = 'Import Data Completed'
    message = 'Your data import has been successful.'
    to_email = settings.DEFAULT_TO_EMAIL
    send_email_notification(mail_subject, message, [to_email])
    return 'Data Imported successfully'

@app.task
def export_data_task(model_name):
    try:
        call_command('exportdata', model_name)
    except Exception as E:
        raise E

    file_path = generate_csv_file(model_name)
    # send email with attechment
    mail_subject = 'Export Data Completed'
    message = 'Your data Export has been successful.'
    to_email = settings.DEFAULT_TO_EMAIL
    send_email_notification(mail_subject, message, [to_email], attechment=file_path)
    return 'Data Exported Successfully'