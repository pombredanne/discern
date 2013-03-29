"""
Define some constants and imports that we will use for all the examples.
"""

#Common imports.
#Requests allows us to make http GET/POST/PUT, etc requests.
#See http://docs.python-requests.org/en/latest/ for documentation
import requests
#JSON is a format for transferring data over the web.  This imports a json handling library.
#See http://en.wikipedia.org/wiki/JSON for information on JSON.
import json

#This tells us where the API is running.
#In order to run the API, you need to navigate to ml-service-api and run python manage.py runserver 127.0.0.1:7999 --nostatic
API_BASE_URL = "http://127.0.0.1:7999"