from celery import shared_task
from django.utils.timezone import now
from datetime import timedelta
from .models import Task

@shared_task
def send_upcoming_deadline_reminders():
    upcoming_time = now() + timedelta(hours=24) #checking for tasks whose deadline is within the range of 24hours.
    tasks = Task.objects.filter(deadline__lte=upcoming_time, status__in=["pending", "ongoing"])
    if tasks.count == 0:
        print("No pending tasks")
    for task in tasks.iterator():
        print(task)
        recipient_list = [task.project.created_by.email] if task.project.created_by.email else []

        if recipient_list:
            print(recipient_list)
        else:
            print("No user found")
    