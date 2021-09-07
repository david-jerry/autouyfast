import os
from urllib import request

from django.core.files import File
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

from autobuyfast.utils.unique_slug_generator import unique_slug_generator

from .models import AutoSearch, Image, WatchCars


@receiver(pre_save, sender=AutoSearch)
def create_post_slug(sender, instance, *args, **kwargs):
	if instance.title and not instance.slug:
		instance.slug = unique_slug_generator(instance)


# @receiver(post_save, sender=AutoSearch)
# def send_car_watch_price_notification(sender, instance, created, *args, **kwargs):
# 	if created and instance.exists():
# 		obj = get_object_or_404(WatchCars, car=instance, active=True)
# 		obj.send_price_change_mail()
		
# @receiver(post_save, sender=AutoSearch)
# def send_car_sold_notification(sender, instance, created, *args, **kwargs):
# 	if created and not instance.available:
# 		obj = get_object_or_404(WatchCars, car=instance, active=True)
		# obj.send_sold_change_mail()


# @receiver(pre_save, sender=Image)
# def convert_img_url_to_image_path(sender, instance, *args, **kwargs):
# 	if instance.img_url and not instance.image:
# 		result = request.urlretrieve(instance.img_url)
# 		instance.image.save(
# 			os.path.basename(instance.img_url),
# 			File(open(result[0], 'rb'))
# 			)
# 		instance.save()
