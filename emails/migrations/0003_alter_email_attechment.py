# Generated by Django 5.0.1 on 2024-01-28 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0002_email_subscriber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='attechment',
            field=models.FileField(blank=True, upload_to='email_attechments/'),
        ),
    ]
