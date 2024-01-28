from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.

class List(models.Model):
    email_list = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.email_list

class Subscriber(models.Model):
    email_list = models.ForeignKey(List, on_delete=models.CASCADE)
    email_address = models.EmailField(max_length=50)

    def __str__(self) -> str:
        return self.email_address

class Email(models.Model):
    email_list = models.ForeignKey(List, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    body = RichTextField()
    attechment = models.FileField(upload_to='email_attechments/', blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.subject