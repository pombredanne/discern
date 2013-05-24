'''
Tutorial - Getting started - create a organization object
Here we create an institution(i.e., Reddit). 
'''

from common_settings import *

session = requests.session()
response = login_to_discern(session)

# create an organization
org_response = session.post(API_BASE_URL + "/essay_site/api/v1/organization/?format=json", 
	data=json.dumps({"organization_name": "Reddit"}),
	headers=headers)

# get the URI for the organization 
#    Let's get the text of the response
organization_object = json.loads(org_response.text)
organization_resource_uri = organization_object['resource_uri']

import pdb; pdb.set_trace()
# create a course and associate it with the organization
course_response = session.post(API_BASE_URL + "/essay_site/api/v1/course/?format=json", 
 	data=json.dumps(
		{"course_name": "Discern Tutorial",
		 "organizations": organization_resource_uri
		}),
 	headers=headers)

