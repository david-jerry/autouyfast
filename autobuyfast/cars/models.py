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
from django.conf import settings
from django.db.models import (
    CASCADE,
    BooleanField,
    IntegerField,
    BigIntegerField,
    PositiveSmallIntegerField,
    SlugField,
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

User = settings.AUTH_USER_MODEL
CAR_MAKE = (
    ('all', 'all'),
    ('ac', 'ac'),
    ('acura', 'acura'),
    ('alfa_romeo', 'alfa romeo'),
    ('allard', 'allard'),
    ('amc', 'amc'),
    ('am_general', 'am general'),
    ('american_motors', 'american motors'),
    ('ariel', 'ariel'),
    ('aston_martin', 'aston martin'),
    ('auburn', 'auburn'),
    ('audi', 'audi'),
    ('austin', 'austin'),
    ('austin_healey', 'austin healey'),
    ('avantimotors', 'avantimotors'),
    ('bentley', 'bentley'),
    ('bmw', 'bmw'),
    ('bugatti', 'bugatti'),
    ('buick', 'buick'),
    ('cadillac', 'cadillac'),
    ('checker', 'checker'),
    ('chevrolet', 'chevrolet'),
    ('chrysler', 'chrysler'),
    ('citroen', 'citroen'),
    ('daewoo', 'daewoo'),
    ('daihatsu', 'daihatsu'),
    ('datsun', 'datsun'),
    ('delahaye', 'delahaye'),
    ('delorean', 'delorean'),
    ('desoto', 'desoto'),
    ('detomaso', 'detomaso'),
    ('dodge', 'dodge'),
    ('eagle', 'eagle'),
    ('edsel', 'edsel'),
    ('essex', 'essex'),
    ('ferrari', 'ferrari'),
    ('fiat', 'fiat'),
    ('fisker', 'fisker'),
    ('ford', 'ford'),
    ('franklin', 'franklin'),
    ('freightliner', 'freightliner'),
    ('genesis', 'genesis'),
    ('geo', 'geo'),
    ('gmc', 'gmc'),
    ('hino', 'hino'),
    ('honda', 'honda'),
    ('hudson', 'hudson'),
    ('hummer', 'hummer'),
    ('hupmobile', 'hupmobile'),
    ('hyundai', 'hyundai'),
    ('infiniti', 'infiniti'),
    ('international', 'international'),
    ('intlharvester', 'intlharvester'),
    ('isuzu', 'isuzu'),
    ('jaguar', 'jaguar'),
    ('jeep', 'jeep'),
    ('jensen', 'jensen'),
    ('kaiser', 'kaiser'),
    ('karma', 'karma'),
    ('kia', 'kia'),
    ('koenigsegg', 'koenigsegg'),
    ('lamborghini', 'lamborghini'),
    ('lancia', 'lancia'),
    ('land_rover', 'land rover'),
    ('lasalle', 'lasalle'),
    ('lexus', 'lexus'),
    ('lincoln', 'lincoln'),
    ('lotus', 'lotus'),
    ('maserati', 'maserati'),
    ('maybach', 'maybach'),
    ('mazda', 'mazda'),
    ('mclaren', 'mclaren'),
    ('mercedes_benz', 'mercedes benz'),
    ('mercury', 'mercury'),
    ('merkur', 'merkur'),
    ('mg', 'mg'),
    ('mini', 'mini'),
    ('mitsubishi', 'mitsubishi'),
    ('morgan', 'morgan'),
    ('morris', 'morris'),
    ('nash', 'nash'),
    ('nissan', 'nissan'),
    ('oldsmobile', 'oldsmobile'),
    ('opel', 'opel'),
    ('packard', 'packard'),
    ('pagani', 'pagani'),
    ('panoz', 'panoz'),
    ('peugeot', 'peugeot'),
    ('plymouth', 'plymouth'),
    ('polestar', 'polestar'),
    ('pontiac', 'pontiac'),
    ('porsche', 'porsche'),
    ('qvale', 'qvale'),
    ('ram', 'ram'),
    ('renault', 'renault'),
    ('rolls_royce', 'rollsroyce'),
    ('rover', 'rover'),
    ('saab', 'saab'),
    ('saleen', 'saleen'),
    ('saturn', 'saturn'),
    ('scion', 'scion'),
    ('shelby', 'shelby'),
    ('smart', 'smart'),
    ('spyker', 'spyker'),
    ('sterling', 'sterling'),
    ('studebaker', 'studebaker'),
    ('subaru', 'subaru'),
    ('sunbeam', 'sunbeam'),
    ('suzuki', 'suzuki'),
    ('tesla', 'tesla'),
    ('toyota', 'toyota'),
    ('triumph', 'triumph'),
    ('tvr', 'tvr'),
    ('volkswagen', 'volkswagen'),
    ('volvo', 'volvo'),
    ('willys', 'willys'),
    ('yugo', 'yugo'),
)
CAR_DOOR = (
    ('all', 'all'),
    ('2', '2-3'),
    ('4', '4'),        
)
CAR_BODY = (
    ('all', 'all'),
    ('sedan', 'sedan'),
    ('coupe', 'coupe'),
    ('convertible', 'convertible'),
    ('wagon', 'wagon'),
    ('hatchback', 'hatchback'),
    ('suv', 'suv'),
    ('minivan', 'minivan'),
    ('truck', 'truck'),
    ('van', 'van'),
)








class AutoSearch(TimeStampedModel):
    car_image = URLField(_("Car Image Url"), max_length=700, blank=True, null=True, unique=False)
    car_stock = CharField(_("Used or New Stock"), max_length=700, blank=True, null=True) 
    car_year = PositiveSmallIntegerField(_("Production Year"), blank=True, null=True) 
    car_title = CharField(_("Car Title"), max_length=700, blank=True, null=True, unique=False) 
    car_url = CharField(_("Car Detail Link"), max_length=700, blank=True, null=True, unique=True) 
    car_mileage = DecimalField(_("Car Mileage"), max_digits=40, blank=True, decimal_places=1, null=True) 
    car_price = DecimalField(_("Car Price"), max_digits=40, blank=True, decimal_places=1, null=True)
    car_history = URLField(_("Car History Link"), max_length=700, blank=True, null=True) 
    car_dealer_name = CharField(_("Car Dealer"), max_length=700, blank=True, default="car dealer name", null=True) 
    # car_dealer_rating = CharField(_("Car Dealer Rating"), max_length=6, blank=True, default="4", null=True) 
    # car_dealer_reviews = CharField(_("Car Dealer No Reviews"), max_length=25, blank=True, default="200 Reviews", null=True) 
    car_dealer_phone = CharField(_("Car Dealer Phone Number"), max_length=16, blank=True, default="+1864756473547", null=True) 

    def __str__(self):
        return self.car_title

    class Meta:
        db_table = 'cars'
        managed = True
        verbose_name = 'Vehicle'
        verbose_name_plural = 'Vehicles'
        ordering = ["-created", "-modified", "-car_year"]