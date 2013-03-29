"""
Example 4: In this example, we will query our models after logging in.
"""

from common_settings import *

login_url = API_BASE_URL + "/essay_site/login/"

#These are the credentials that we created in the previous example.
data = {
    'username' : 'test',
    'password' : 'test'
}

#We need to explicitly define the content type to let the API know how to decode the data we are sending.
headers = {'content-type': 'application/json'}

#A session allows us to store cookies and other persistent information.
#In this case, it lets the server keep us logged in and make requests as a logged in user.
session = requests.Session()
response = session.post(login_url, data=json.dumps(data),headers=headers)
print("Status Code: {0}".format(response.status_code))

#Now, let's try to get the schema for a single model.
response = session.get(API_BASE_URL + "/essay_site/api/v1/essay/?format=json")

#This should get a 401 error if you are not logged in.
print("Status Code: {0}".format(response.status_code))

