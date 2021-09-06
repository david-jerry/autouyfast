import os
import random
from datetime import datetime

import readtime
from category.models import Category, Tag
from comment.models import Comment
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import (
    CASCADE,
    SET_NULL,
    BigIntegerField,
    BooleanField,
    CharField,
    DateField,
    DateTimeField,
    DecimalField,
    EmailField,
    FileField,
    ForeignKey,
    ImageField,
    IntegerField,
    ManyToManyField,
    OneToOneField,
    PositiveSmallIntegerField,
    SlugField,
    TextChoices,
    TextField,
    URLField,
    UUIDField,
)
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField
# Third party installs
from model_utils.models import TimeStampedModel
from tinymce.models import HTMLField

from .managers import FaqManager

User = settings.AUTH_USER_MODEL

# Create your models here.

class Faq(TimeStampedModel):
    DRAFT = "draft"
    PUBLISHED = "published"
    STATUS = (
        (DRAFT, "Draft"),
        (PUBLISHED, "Published")
    )
    title = CharField(_("Post Title"), max_length=500, blank=True, null=True, unique=True)
    content = HTMLField(_("Post Content"), null=True, blank=True)
    status = CharField(_("Status"), max_length=100, blank=True, null=True, choices=STATUS, default=DRAFT)
    objects = FaqManager()

    def __str__(self):
        return self.title


    class Meta:
        managed = True
        verbose_name = "Faq"
        verbose_name_plural = "Faqs"
        ordering = ["-created", "-modified"]


class EmailSubscribe(TimeStampedModel):
    email = EmailField(_("Email Please"), blank=True, null=True)
    active = BooleanField(_("Email Subscription Active"), default=False)

    def __str__(self):
        return f"{self.email} just subscribed to the mailing list"

    class Meta:
        managed = True
        verbose_name = "Email Subscriber"
        verbose_name_plural = "Email Subscribers"
        ordering = ["-created", "-modified"]

    