from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.shortcuts import get_object_or_404
from django.utils import timezone


class FaqManager(models.Manager):
    def get_queryset(self):
        # All faqs
        return super().get_queryset()

    def all_faq(self):
        # All faqs
        return super().get_queryset().filter(status="published")

    def recent_faqs(self):
        # All recent faqs
        return super().get_queryset().filter(status="published", created__lte=timezone.now()).order_by("-created")
