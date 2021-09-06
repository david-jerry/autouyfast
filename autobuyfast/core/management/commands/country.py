# import json

# import requests
# from django.conf import settings
# from django.contrib.auth import authenticate, get_user_model, login
# from django.core.exceptions import ObjectDoesNotExist
# from django.core.management.base import BaseCommand
# from django.http import JsonResponse
# from django.utils.translation import gettext_lazy as _

# from autobuyfast.core.models import Country

# # from requests_html import HTMLSession


# User = get_user_model()


# class Command(BaseCommand):
#     help = _("Get all countries supported by restcountries")

#     def handle(self, *args, **kwargs):
#         url = "https://restcountries.eu/rest/v2/all"
#         headers = {
#             "Authorization": "Bearer ",
#             "Content-Type": "application/json",
#             "Accept": "application/json",
#         }
#         # datum = {"country": "nigeria", "use_cursor": True, "perPage": 100}
#         # x = requests.get(url, data=json.dumps(datum), headers=headers)
#         x = requests.get(url, headers=headers)
#         if x.status_code != 200:
#             return str(x.status_code)

#         results = x.json()
#         # for i in results["data"]:
#         for i in results:
#             name = i["name"]
#             country_name = name.replace('(', '').replace(')', '').replace('-', '').replace(',', '')
#             print(country_name)
#             country_capital = i["capital"]
#             country_region = i["region"]
#             country_sub_region = i["subregion"]
#             country_population = i["population"]
#             country_call_code = i["callingCodes"]
#             country_flag = i["flag"]
#             iso_code = i["numericCode"]
#             try:
#                 Country.objects.create(name=str(country_name), capital=str(country_capital), flag=str(country_flag), region=str(country_region), sub_region=str(country_sub_region), population=str(country_population), call_code=str(country_call_code), iso_code=str(iso_code))
#                 print(f"{country_name} Created Successfully")
#             except:
#                 print(f"{country_name} Exists")
#         self.stdout.write("Countries Saved Successfully.")
