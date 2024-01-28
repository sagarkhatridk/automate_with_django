from django.shortcuts import render, redirect
from .tasks import send_email_task
from .forms import EmailForm
from django.contrib import messages
from django.conf import settings
from .models import Subscriber

# Create your views here.
def send_email(request):
    if request.method == 'POST':
        email_form = EmailForm(request.POST, request.FILES)
        if email_form.is_valid():
            email_form = email_form.save()

            # TODO send an Email
            mail_subject = request.POST.get('subject')
            message = request.POST.get('body')

            # Access the selected email list
            email_list = email_form.email_list

            # extract email addresses from the Subscripber model in the selected emai list
            subscribers = Subscriber.objects.filter(email_list=email_list)
            to_email = [email.email_address for email in subscribers]

            if email_form.attechment:
                attechment = email_form.attechment.path
            else:
                attechment = None

            #  hand ove email sending task to celery
            send_email_task.delay(mail_subject, message, to_email, attechment)

            messages.success(request, 'Email Send Successfully')
            return redirect('send_email')
        else:
            print(email_form.errors)

    else:
        email_form = EmailForm()
        context = {
            'email_form':email_form
        }
        return render(request, 'emails/send-email.html', context)