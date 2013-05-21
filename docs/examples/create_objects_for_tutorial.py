'''
Tutorial - Getting started - creating objects
Here we create an institution(i.e., reddit), a course(i.e., learning about Discern), and a problem object. 
'''

from common_settings import *

#This is the same login code that we used previously
login_url = API_BASE_URL + "/essay_site/login/"
login_url_data = {
    'username' : 'test',
    'password' : 'test'
}
headers = {'content-type': 'application/json'}
session = requests.session()
response = session.post(login_url, data=json.dumps(login_url_data),headers=headers)

# Now that we are logged in, let's create...


# an organization
response = session.post(API_BASE_URL + "/essay_site/api/v1/organization/?format=json", 
	data=json.dumps({"organization_name": "Dr. Mbogo's instituting of dentistry"}),
	headers=headers)
import pdb; pdb.set_trace()

# a course 
try:
	response = session.post(API_BASE_URL + "/essay_site/api/v1/course/?format=json", 
		data=json.dumps({"course_name": "learning about Discern's APIs"}),
		headers=headers)
except: 
	import pdb; pdb.set_trace()
