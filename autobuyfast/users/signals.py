from allauth.account.signals import user_signed_up
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage, send_mail, send_mass_mail
from django.db.models import F
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy

from .models import AlertSetting, Profile, Testimonial

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, *args, **kwargs):
	if created:
		Profile.objects.get_or_create(user = instance)
		AlertSetting.objects.get_or_create(user = instance)
		print('****', "creating user profile works")
	
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, *args, **kwargs):
	if created:
		instance.userprofile.save()
		instance.useralerts.save()
		print('_-----', "saving users profiles working")	


# @receiver(pre_save, sender=Testimonial)
# def mark_testified_true(sender, instance, *args, **kwargs):
# 	if instance:
# 		instance.user.update(has_testified=True)


# @receiver(user_signed_up)
# def user_signed_up(request, user, *args, **kwargs):
#     send_mail(
        
#     )
