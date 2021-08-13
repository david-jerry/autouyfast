from urllib.request import urlopen

# import json
import requests
# from urllib.request import urlopen
from bs4 import BeautifulSoup
from django.contrib.auth import authenticate, get_user_model, login
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
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
            nxt_pg = pages.find('a', {'id': 'next_paginate'})
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
            n = 0 + 1
            for car in car_cards:
                car_id = n
                car_def_image = car.find('div', class_="gallery-wrap").find('div', class_="image-wrap").find('a').find('img')['src']
                car_stock = car.find('p', class_='stock-type').text
                car_title = car.find('a', class_='vehicle-card-link').find('h2').text
                car_year = car_title[:4]
                car_url = 'https://www.cars.com' + str(car.find('a', class_='vehicle-card-link')['href'])
                car_mileage = car.find('div', class_='mileage').text.replace(',','').replace('mi','').replace(' .','')
                car_price = car.find('span', class_='primary-price').text.replace(',','').replace('$','').replace(' ','')
                car_history_report_url = 'https://www.cars.com' + str(car.find('div', class_='vehicle-deeplink').find('a')['href'])
                car_dealer_name = car.find('div', class_='dealer-name').find('strong').text
                car_dealer_phone = car.find('a', class_='sds-button--secondary contact-by-phone')['href'][4:]
                
                if car_url:
                    html_content = s.get(car_url)
                    detail_soup = BeautifulSoup(html_content.content, features='html.parser')
                    detail_cars = detail_soup.find('dl', class_="fancy-description-list")
                    ext_color = detail_cars.find("dt",text="Exterior color").findNext("dd").string
                    int_color = detail_cars.find("dt",text="Interior color").findNext("dd").string
                    drive_train = detail_cars.find("dt",text="Drivetrain").findNext("dd").string
                    fuel_type = detail_cars.find("dt",text="Fuel type").findNext("dd").string
                    vin = detail_cars.find("dt",text="VIN").findNext("dd").string
                    engine = detail_cars.find("dt",text="Engine").findNext("dd").string
                    transmission = detail_cars.find("dt",text="Transmission").findNext("dd").string
                    
                    # Car description and features
                    feature = detail_soup.find('h2', text="Features").findNext('dl', class_="fancy-description-list")
                    car_images = detail_soup.find_all('img', class_="row-pic")
                    for img in car_images:
                        image = img['src']

                
                try:
                    AutoSearch.objects.create(
                        car_url = car_url,
                        car_vin = vin,
                        dealer = User(id=1),
                        car_stock = car_stock,
                        car_year = int(car_year),
                        title = car_title,
                        slug = "",
                        car_mileage = float(car_mileage),
                        car_price = float(car_price),
                        car_sub_price=float(0.00),
                        car_history = car_history_report_url,
                        car_def_image = car_def_image,
                        car_dealer_name = car_dealer_name,
                        car_dealer_phone = car_dealer_phone,
                        car_transmission = transmission,
                        car_ext_color = ext_color,
                        car_int_color = int_color,
                        car_drive_train = drive_train,
                        car_fuel_type = fuel_type,
                        car_engine = engine,
                        # car_safety = car_safety,
                        # car_body = car_body,
                        # car_make = car_make,
                        # car_entertainment = None,
                        # car_convenience = None,
                        seller_note = "",
                    )
                    print(f'{car_title} was added')
                    try:
                        Image.objects.create(
                            car = AutoSearch.objects.get(pk=car_id),
                            image = image
                        )
                    except:
                        print(f"{car_title} image can't be saved")
                except:
                    print(f'{car_title} already exists')


                    

        self.stdout.write("Car Scraping Completed Successfully.")
