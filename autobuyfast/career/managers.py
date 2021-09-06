from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.shortcuts import get_object_or_404
from django.utils import timezone


class CareerManager(models.Manager):
    def get_queryset(self):
        # All posts
        return super().get_queryset()

    def all(self):
        # All posts
        return super().get_queryset().filter(status="published")

    def recent_careers(self):
        # All recent posts
        return super().get_queryset().filter(status="published", created__lte=timezone.now()).order_by("-created")


