from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta


class CarManager(models.Manager):
    def get_queryset(self):
        # All posts
        return super().get_queryset()

    def all_posts(self):
        # All posts
        return super().get_queryset().filter(status="published")

    def recent_posts(self):
        # All posts
        return super().get_queryset().filter(status="published", created__lte=timezone.now()).order_by("-created")




class WatchCarsEmailSend(models.query.QuerySet):
    def notifiable(self):
        now = timezone.now()
        start_range = now - timedelta(days=)

class WatchCarManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
