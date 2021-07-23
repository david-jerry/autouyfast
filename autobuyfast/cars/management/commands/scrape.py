from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
# import json
import requests
from requests_html import HTMLSession 
from autobuyfast.cars.models import AutoSearch
from urllib.request import urlopen

# from urllib.request import urlopen
from bs4 import BeautifulSoup



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
                car_image = car.find('div', class_="gallery-wrap").find('div', class_="image-wrap").find('a').find('img')['src']
                car_stock = car.find('p', class_='stock-type').text
                car_title = car.find('a', class_='vehicle-card-link').find('h2').text
                car_year = car_title[:4]
                car_url = 'https://www.cars.com' + str(car.find('a', class_='vehicle-card-link')['href'])
                car_mileage = car.find('div', class_='mileage').text.replace(',','').replace('mi','').replace(' .','')
                car_price = car.find('span', class_='primary-price').text.replace(',','').replace('$','').replace(' ','')
                car_history_report_url = 'https://www.cars.com' + str(car.find('div', class_='vehicle-deeplink').find('a')['href'])
                car_dealer_name = car.find('div', class_='dealer-name').find('strong').text
                car_dealer_phone = car.find('a', class_='sds-button--secondary contact-by-phone')['href'][4:]

                
                car_model = AutoSearch.objects.filter(car_dealer_phone=car_dealer_phone,car_title=car_title,car_image=car_image,car_stock=car_stock,car_year=car_year,car_url=car_url,car_mileage=car_mileage,car_price=car_price,car_history=car_history_report_url,car_dealer_name=car_dealer_name)
                
                if not car_model:
                    AutoSearch.objects.get_or_create(
                        car_image = car_image,
                        car_stock = car_stock,
                        car_year = int(car_year),
                        car_url = car_url,
                        car_mileage = float(car_mileage),
                        car_price = float(car_price),
                        car_history = car_history_report_url,
                        car_dealer_name = car_dealer_name,
                        car_dealer_phone = car_dealer_phone,
                        car_title = car_title
                    )
                    print(f'{car_title} was added')
                else:
                    print(f'{car_title} already exists')


                    

        self.stdout.write("Car Scraping Completed Successfully.")
