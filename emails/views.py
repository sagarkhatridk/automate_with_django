from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .tasks import send_email_task
from .forms import EmailForm
from django.contrib import messages
from django.conf import settings
from .models import Sent, Subscriber, Email, EmailTracking
from django.db.models import Sum
from django.utils import timezone


# Create your views here.
def send_email(request):
    if request.method == "POST":
        email_form = EmailForm(request.POST, request.FILES)
        if email_form.is_valid():
            email = email_form.save()

            # TODO send an Email
            mail_subject = request.POST.get("subject")
            message = request.POST.get("body")

            # Access the selected email list
            email_list = email.email_list

            # extract email addresses from the Subscripber model in the selected emai list
            subscribers = Subscriber.objects.filter(email_list=email_list)
            to_email = [email.email_address for email in subscribers]

            if email.attechment:
                attechment = email.attechment.path
            else:
                attechment = None

            email_id = email.id

            #  hand ove email sending task to celery
            send_email_task.delay(mail_subject, message, to_email, attechment, email_id)

            messages.success(request, "Email Send Successfully")
            return redirect("send_email")
        else:
            print(email_form.errors)

    else:
        email_form = EmailForm()
        context = {"email_form": email_form}
        return render(request, "emails/send-email.html", context)


def track_click(request, unique_id):
    try:
        email_tracking = EmailTracking.objects.get(unique_id=unique_id)
        url = request.GET.get("url")
        # Check if the clicked_at field is already set or not
        if not email_tracking.clicked_at:
            email_tracking.clicked_at = timezone.now()
            email_tracking.save()
        return HttpResponseRedirect(url)
    except:
        return HttpResponse("Email Tracking record not found.")


def track_open(request, unique_id):
    try:
        email_tracking = EmailTracking.objects.get(unique_id=unique_id)
        # Check if the opened_at field is already set or not
        if not email_tracking.opened_at:
            email_tracking.opened_at = timezone.now()
            email_tracking.save()
            return HttpResponse("Email Opened")
        else:
            print("Email already Opened.")
            return HttpResponse("Email already Opened.")
    except:
        return HttpResponse("Email Tracking record not found.")


def track_stats(request, pk):
    email = get_object_or_404(Email, pk=pk)
    sent = Sent.objects.get(email=email)
    context = {
        "email": email,
        "total_sent": sent.total_sent,
    }
    return render(request, "emails/track_stats.html", context)


def track_dashboard(request):
    emails = (
        Email.objects.all()
        .annotate(total_sent=Sum("sent__total_sent"))
        .order_by("-sent_at")
    )
    context = {"emails": emails}
    return render(request, "emails/track_dashboard.html", context)
