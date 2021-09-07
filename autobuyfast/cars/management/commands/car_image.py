# from urllib.request import urlopen
import os
from decimal import Decimal
from urllib.request import urlopen

# import json
import requests
from bs4 import BeautifulSoup
from django.contrib.auth import authenticate, get_user_model, login
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify
from requests_html import HTMLSession

User = get_user_model()

from autobuyfast.cars.models import (  # Body,; Convenience,; Entertainment,; Make,; Safety,; Seating,; Stock,; Year,
    AutoSearch,
    Image,
)


class Command(BaseCommand):
    help = "Collect Cars from Cars.com"

    # define logic of command
    def handle(self, *args, **options):

        # get html link
        User.objects.get_or_create(username="cars", email="cars@mail.com"),
        n = [0,1,2,3,4,5]
        for i, id in enumerate(n):
            car_id = id
            # if i+1 % 5 == 0:
            #     print("i information", i)
                
        # print(car_id)
        s = HTMLSession()
        headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
        url = "https://www.cars.com/shopping/results/?body_style_slugs[]=&dealer_id=&list_price_max=175000&list_price_min=&makes[]=&maximum_distance=all&mileage_max=&only_with_photos=true&page_size=3&sort=best_match_desc&stock_type=all&year_max=&year_min=2001&zip=00674"

        # convert to bs4
        def getdata(url):
            r = s.get(url)
            soup = BeautifulSoup(r.html.html, 'html.parser')
            return soup
        
        def getnextpage(soup):
            # this will return the next page URL
            pages = soup.find('div', {'class': 'sds-pagination__controls'})
            # nxt_pg = pages.find('a', {'id': 'next_paginate'})
            lst_pg = pages.find('button', {'id':'next_paginate'})
            if not lst_pg:
                url = 'https://www.cars.com' + str(soup.find('a', {'id': 'next_paginate'})['href'])
                return url

        while True:
            data = getdata(url)
            url = getnextpage(data)
            if not url:
                break

            # grab all vehicle card
            html_content = s.get(url)
            soup = BeautifulSoup(html_content.content, features='html.parser')
            car_cards = soup.find_all('div', class_="vehicle-card-main")
            for car in car_cards:
                car_title = car.find('a', class_='vehicle-card-link').find('h2').text
                car_slug = slugify(car_title)
                car_url = 'https://www.cars.com' + str(car.find('a', class_='vehicle-card-link')['href'])
                
                inner_content = s.get(car_url)
                detail_soup = BeautifulSoup(inner_content.content, features='html.parser')
                car_images = detail_soup.find_all('img', class_="swipe-main-image")
                for img in car_images[1:]:
                    image = img['data-src']
                    c_id = get_object_or_404(AutoSearch, slug=car_slug)
                    # try:
                    Image.objects.create(
                        car = AutoSearch(id=c_id.id),
                        img_url = image
                    )
                    print(f"Images added to {car_title}")
                    # except:
                    #     print(f"No vehicle to associate the images to {car_title}")
                

        self.stdout.write("Car Scraping Completed Successfully.")
