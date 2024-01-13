"""
Insert data to database command.
"""
from django.core.management.base import BaseCommand
from dataentry.models import Student

class Command(BaseCommand):
    """Insert data to the database custom command."""

    help = 'Intert data to the database.'

    def handle(self, *args, **kwargs):
        """custom logic for what this command will do."""

        dataset = [
            {'roll_no':1002, 'name':'Darshan', 'age':20},
            {'roll_no':1003, 'name':'Krishna', 'age':21},
            {'roll_no':1004, 'name':'Bhavik', 'age':22},
            {'roll_no':1005, 'name':'Vrushabh', 'age':24},
            {'roll_no':1006, 'name':'Sarthak', 'age':23},
        ]

        for data in dataset:
            roll_no = data['roll_no']
            existing_record = Student.objects.filter(roll_no=roll_no).exists()
            if not existing_record:
                Student.objects.create(
                    roll_no=roll_no,
                    name=data['name'],
                    age=data['age']
                )
            else:
                self.stdout.write(self.style.WARNING(f'Student with roll no {roll_no} already exists.'))
        self.stdout.write(self.style.SUCCESS('Data Inserted Successfully.'))