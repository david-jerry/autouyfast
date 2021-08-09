from __future__ import absolute_import

# development system imports
import datetime
import os
import random
import uuid
from decimal import Decimal

# Third partie imports
from countries_plus.models import Country
# django imports
from django.contrib.auth.models import AbstractUser
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
    OneToOneField,
    TextChoices,
    TextField,
    URLField,
    UUIDField,
)
from django.template.loader import get_template, render_to_string
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField
# Third party installs
from model_utils.models import TimeStampedModel
from tinymce.models import HTMLField

# REGEX Expressions for validation
SSN_REGEX = "^(?!666|000|9\\d{2})\\d{3}-(?!00)\\d{2}-(?!0{4}\\d{4}$)"
NUM_REGEX = "^[0-9]*$"
ABC_REGEX = "^[A-Za-z]*$"


# Image upload folders
def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def banner_image(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = "{new_filename}{ext}".format(new_filename=new_filename, ext=ext)
    return "banner/{new_filename}/{final_filename}".format(
        new_filename=new_filename, final_filename=final_filename
    )


def profile_image(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = "{new_filename}{ext}".format(new_filename=new_filename, ext=ext)
    return "profile/{new_filename}/{final_filename}".format(
        new_filename=new_filename, final_filename=final_filename
    )


class User(AbstractUser):
    """Default user for autobuyfast."""

    #: First and last name do not cover name patterns around the globe
    phone_no = CharField(_("Phone Number"), blank=True, max_length=13)
    is_seller = BooleanField(_('Are you a dealer?'), default=True)
    has_testified = BooleanField(_("Has this user testified to our service?"), default=False)

    def initials(self):
        if self.first_name and self.last_name:
            fname = self.first_name[0].upper()
            lname = self.last_name[0].upper()
            initials = f"{fname} {lname}"
        else:
            uname = self.username[0:1].upper()
            initials = f"{uname}"
        return initials

    def fullname(self):
        if self.first_name and self.last_name:
            fullname = f"{self.first_name} {self.last_name}"
        else:
            fullname = f"{self.username}"
        return fullname

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


class Profile(TimeStampedModel):
    ONE = "favourite actor"
    TWO = "pet's name"
    THREE = "first school attended"
    FOUR = "place of birth"
    FIVE = "mother's maiden name"
    QUESTION = (
        (ONE, _("Who is your favourite actor?")),
        (TWO, _("What is your pet's name?")),
        (THREE, _("What is the name of the first school attended?")),
        (FOUR, _("Where is your place of birth?")),
        (FIVE, _("What is your mother's maiden name?"))
    )
    user = OneToOneField(User, on_delete=CASCADE, related_name="userprofile")
    dealership_name = CharField(_("Company Name"), max_length=500, null=True, blank=True, unique=True)
    bio = HTMLField(_("What services will buyers find appealing from you?"), null=True, blank=True)
    website = URLField(_("Website URI"), null=True, blank=True, unique=True)
    profile_display = ResizedImageField(size=[120, 120], quality=64.15, crop=['middle', 'center'], upload_to=profile_image, force_format='JPEG', help_text="Image should be squared and sized 120px X 120px")
    banner_display = ResizedImageField(size=[1280, 300], quality=64.15, crop=['middle', 'center'], upload_to=banner_image, force_format='JPEG', help_text="Image should be cropped and sized 1280px X 300px")
    country = ForeignKey(Country, on_delete=CASCADE, related_name="dealercountry", null=True, blank=True)
    address = CharField(_("Address"), max_length=500, null=True, blank=True)
    city = CharField(_("City"), max_length=500, null=True, blank=True)
    zipcode = CharField(_("Zipcode"), max_length=500, null=True, blank=True)
    member_since = DateField(_("Membership Age"), default=datetime.datetime.now)
    security_quest = CharField(_("Security Question"), choices=QUESTION, default=FIVE, max_length=47)
    security_answer = CharField(_("Security Answer"), max_length=500, null=True, blank=True)

    def __str__(self):
        return self.user.fullname

    class Meta:
        managed = True
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        ordering = ["-created", "-modified"]

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.user.username})


class AlertSetting(TimeStampedModel):
    user = OneToOneField(User, on_delete=CASCADE, related_name="useralerts")
    newsletter_notif = BooleanField(_("Subscribe to Newsletter?"), default=False)
    search_notif = BooleanField(_("Send Email When Saved Search is deleted?"), default=False)
    car_sold_notif = BooleanField(_("Send Email When Saved car is sold?"), default=False)
    car_price_notif = BooleanField(_("Send Email When Saved car price has been reduced?"), default=False)
    
    def __str__(self):
        return self.user.fullname

    class Meta:
        managed = True
        verbose_name = "Alert"
        verbose_name_plural = "Alerts"
        ordering = ["-created", "-modified"]



class Testimonial(TimeStampedModel):
    user = ForeignKey(User, on_delete=SET_NULL, null=True, related_name="usertestimonial")
    testimony = CharField(_("Testimony"), max_length=800, blank=True, null=True)
    active = BooleanField(default=False)
    
    def __str__(self):
        return self.user.fullname

    class Meta:
        managed = True
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"
        ordering = [ "-created", "-modified"]
