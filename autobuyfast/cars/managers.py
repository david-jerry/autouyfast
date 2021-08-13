from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.shortcuts import get_object_or_404
from django.utils import timezone


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


class WatchCarManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
