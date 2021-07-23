#!/bin/bash -ex

# Run migrate and fix scraped data into the database for cars scrape
python manage.py migrate

python manage.py scrape