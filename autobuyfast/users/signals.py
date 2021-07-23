from allauth.account.signals import user_signed_up
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage, send_mail, send_mass_mail
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Buyer, Dealer

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	print('****', created)
	if instance.is_buyer:
		Buyer.objects.get_or_create(user = instance)
	else:
		Dealer.objects.get_or_create(user = instance)
	
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	print('_-----')	
	# print(instance.internprofile.bio, instance.internprofile.location)
	if instance.is_buyer:
		instance.buyerprofile.save()
	else:
		Dealer.objects.get_or_create(user = instance)


@receiver(user_signed_up)
def user_signed_up(request, user, *args, **kwargs):
    send_mail(
        
    )