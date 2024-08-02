
from celery import shared_task
from django.utils import timezone
from .models import Project

@shared_task
def delete_expired_projects():
    now = timezone.now()
    expired_projects = Project.objects.filter(dateOfFinish__lt=now)
    expired_projects.delete()