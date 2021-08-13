from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from autobuyfast.utils.unique_slug_generator import unique_slug_generator

from .models import AutoSearch, WatchCars


@receiver(pre_save, sender=AutoSearch)
def create_post_slug(sender, instance, *args, **kwargs):
	if instance.title and not instance.slug:
		instance.slug = unique_slug_generator(instance)


@receiver(post_save, sender=AutoSearch)
def send_car_watch_price_notification(sender, instance, created, *args, **kwargs):
	if created:
		obj = WatchCars.objects.get(car=instance, active=True)
		obj.send_price_change_mail()
		
@receiver(post_save, sender=AutoSearch)
def send_car_sold_notification(sender, instance, created, *args, **kwargs):
	if created and not instance.available:
		obj = WatchCars.objects.filter(car=instance, active=True)
		obj.send_sold_change_mail()
