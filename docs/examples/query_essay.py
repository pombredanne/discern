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
session = requests.session()
response = session.post(login_url, data=json.dumps(data),headers=headers)
print("Status Code: {0}".format(response.status_code))

#Now, let's try to get all the essay models that we have access to.
response = session.get(API_BASE_URL + "/essay_site/api/v1/essay/?format=json")

#This should get a 401 error if you are not logged in, and a 200 if you are.
print("Status Code: {0}".format(response.status_code))

#At this point, we will get a response from the server that lists all of the essay objects that we have created.
print("Response from server: {0}".format(response.text))

#We have yet to create any essay objects, so we will need to add some in before they can be properly displayed back to us.




