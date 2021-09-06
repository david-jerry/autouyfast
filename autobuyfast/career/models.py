import os
import random
from datetime import datetime

import readtime
from category.models import Category, Tag
from comment.models import Comment
from countries_plus.models import Country
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

from .managers import CareerManager

# from .validators import file_validator

# REGEX Expressions for validation

# Image upload folders
def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def cv_file_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = "{new_filename}{ext}".format(new_filename=new_filename, ext=ext)
    return "applicant_cv/{new_filename}/{final_filename}".format(
        new_filename=new_filename, final_filename=final_filename
    )


User = settings.AUTH_USER_MODEL

# Create your models here.
class Career(TimeStampedModel):
    DRAFT = "draft"
    PUBLISHED = "published"
    STATUS = (
        (DRAFT, "Draft"),
        (PUBLISHED, "Published")
    )
    TYPE = (
        ("office", "Office"),
        ("remote", "Remote"),
        ("hybrid", "Hybrid")
    )
    title = CharField(_("Career Title"), max_length=500, blank=True, null=True, unique=True)
    position = CharField(_("Career Position"), max_length=500, blank=True, null=True, unique=True)
    type = CharField(_("Career Type"), max_length=10, blank=True, null=True,  choices=TYPE, default="office")
    slug = SlugField(max_length=700, blank=True, null=True, unique=True)
    content = HTMLField(_("Career Details and Requirements"), null=True, blank=True)
    status = CharField(_("Status"), max_length=100, blank=True, null=True, choices=STATUS, default=DRAFT)
    objects = CareerManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("careers:detail", kwargs={"slug": self.slug})



    class Meta:
        managed = True
        verbose_name = "Career"
        verbose_name_plural = "Careers"
        ordering = ["-created", "-modified"]

class CareerApply(TimeStampedModel):
    career = ForeignKey(Career, on_delete=SET_NULL, null=True)
    cv = FileField(_("Upload Your CV"), upload_to=cv_file_path, null=True, blank=False)
    name = CharField(_("Your Fullname"), max_length=500, blank=False, null=True)
    email = EmailField(_("Your Email"), null=True, blank=False, unique=True)
    nationality = ForeignKey(Country, null=True, on_delete=SET_NULL)
    address = CharField(_("Your Residential Address"), max_length=700, null=True, blank=False)
    linkedin = URLField(_("Your Linkedin Profile"), blank=False, null=True)
    facebook = URLField(_("Your Facebook Profile"), blank=False, null=True)
    twitter = URLField(_("Your Twitter Profile"), blank=False, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        managed = True
        verbose_name = "Career Application"
        verbose_name_plural = "Career Applications"
        ordering = ["-created", "-modified"]
    