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
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Third party installs
from model_utils.models import TimeStampedModel
from tinymce.models import HTMLField

# Developer defined imports
# from ..utils.validators import (
#     validate_uploaded_image_extension,
#     validate_uploaded_pdf_extension,
# )

# REGEX Expressions for validation
SSN_REGEX = "^(?!666|000|9\\d{2})\\d{3}-(?!00)\\d{2}-(?!0{4}\\d{4}$)"
NUM_REGEX = "^[0-9]*$"
ABC_REGEX = "^[A-Za-z]*$"


# Image upload folders
def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def idcard_image(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = "{new_filename}{ext}".format(new_filename=new_filename, ext=ext)
    return "idcard/{new_filename}/{final_filename}".format(
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
    is_buyer = BooleanField(_('Do you want to just buy cars?'), default=True)

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

class Buyer(TimeStampedModel):
    user = OneToOneField(User, on_delete=CASCADE, related_name="buyerprofile")
    country = ForeignKey(Country, on_delete=CASCADE, related_name="buyercountry", null=True, blank=True)

class Dealer(TimeStampedModel):
    user = OneToOneField(User, on_delete=CASCADE, related_name="dealerprofile")
    dealership_name = CharField(_("Company Name"), max_length=500, null=True, blank=True)
    country = ForeignKey(Country, on_delete=CASCADE, related_name="dealercountry", null=True, blank=True)
    bio = HTMLField(_("What services will buyers find appealing from you?"), null=True, blank=True)
    member_since = DateField(_("Membership Age"), default=datetime.datetime.now)

