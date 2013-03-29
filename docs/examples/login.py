import requests
import json

API_BASE_URL = "http://127.0.0.1:7999"

#We can use api key authentication or django session authentication.  In this case, we will login with the django session.

login_url = API_BASE_URL + "/essay_site/login/"

#In order to create a user, we need to define a username and a password
data = {
    'username' : 'test',
    'password' : 'test'
}

#We need to explicitly define the content type to let the API know how to decode the data we are sending.
headers = {'content-type': 'application/json'}

#Now, let's try to get the schema for the create user model.
response = requests.post(login_url, data=json.dumps(data),headers=headers)