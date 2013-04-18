"""
Run me with:
    python manage.py test
"""
import json
import unittest
from datetime import datetime
import logging
import urlparse

from django.contrib.auth.models import User
from django.test.client import Client
import requests
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from models import Organization, Course, Problem, Essay, EssayGrade, UserProfile
from django.core.urlresolvers import reverse
from django.core.management import call_command
from ml_grading import ml_model_creation

log = logging.getLogger(__name__)

def run_setup():
    """
    Setup function
    """
    #Refresh haystack index
    call_command('update_index', interactive=False)
    #Check to see if test user is created and create if not.
    if(User.objects.filter(username='test').count() == 0):
        user = User.objects.create_user('test', 'test@test.com', 'test')
        user.save()

def delete_all():
    """
    Teardown function to delete everything in DB
    """
    Organization.objects.all().delete()
    Course.objects.all().delete()
    #This should cascade down and delete all associated essays and essaygrades
    Problem.objects.all().delete()

def get_urls(resource_name):
    """
    Get endpoint and schema urls through url reverse
    resource_name - The name of an api resource.  ie "organization"
    """
    endpoint = reverse("api_dispatch_list", kwargs={'api_name': 'v1','resource_name': resource_name})
    schema = reverse("api_get_schema", kwargs={'api_name': 'v1','resource_name': resource_name})
    return endpoint,schema

def get_first_resource_uri(type):
    """
    Get the first resource uri of an object of a given type
    type - the type of resource as defined in the api, ie "organization"
    """
    #Create a client and login
    c = login()
    #Get the urls needed
    endpoint, schema = get_urls(type)
    #Get the data on all models from the endpoint
    data = c.get(endpoint, data={'format' : 'json'})
    #Grab a single object, and get the resource uri from it
    object = json.loads(data.content)['objects'][0]
    resource_uri = object['resource_uri']
    return resource_uri

def create_object(type, object):
    """
    Create an object of a given type if the data is given
    type - the type of resource as defined in the api, ie "organization"
    object - the data to post to the server to create the object of type
    """
    c = login()
    endpoint, schema = get_urls(type)
    result = c.post(endpoint, json.dumps(object), "application/json")
    return result

def login():
    """
    Creates a client, logs in as the test user, and returns the client
    """
    c = Client()
    c.login(username='test', password='test')
    return c

def create_organization():
    """
    Create an organization
    """
    organization_object =  {"name" : "edX"}
    result = create_object("organization", organization_object)
    organization_resource_uri = json.loads(result.content)['resource_uri']
    return organization_resource_uri

def create_course():
    """
    Create a course
    """
    course_object = {'course_name' : "edx_test"}
    result = create_object("course", course_object)
    course_resource_uri = json.loads(result.content)['resource_uri']
    return course_resource_uri

def create_problem():
    """
    Create a problem
    """
    course_resource_uri = create_course()
    problem_object = {'courses' : [course_resource_uri], 'max_target_scores' : json.dumps([1,1])}
    result = create_object("problem", problem_object)
    problem_resource_uri = json.loads(result.content)['resource_uri']
    return problem_resource_uri

def create_essay():
    """
    Create an essay
    """
    problem_resource_uri = create_problem()
    essay_object = {'problem' : problem_resource_uri, 'essay_text' : "This is a test essay!", 'essay_type' : 'train'}
    result = create_object("essay", essay_object)
    essay_resource_uri = json.loads(result.content)['resource_uri']
    return essay_resource_uri

def create_essaygrade():
    """
    Create an essaygrade
    """
    essay_resource_uri = create_essay()
    essaygrade_object = {'essay' : essay_resource_uri, 'target_scores' : json.dumps([1,1]), 'grader_type' : "IN", 'feedback' : "Was ok.", 'success' : True}
    result = create_object("essaygrade", essaygrade_object)
    essaygrade_resource_uri = json.loads(result.content)['resource_uri']
    return essaygrade_resource_uri

model_registry = {
    'course' : create_course,
    'problem' : create_problem,
    'essay' : create_essay,
    'organization' : create_organization,
    'essaygrade' : create_essaygrade,
}

def create_ml_essays(type, count):
    problem_resource_uri = create_problem()
    for i in xrange(0,count):
        essay_object = {'problem' : problem_resource_uri, 'essay_text' : "This is a test essay!", 'essay_type' : type}
        result = create_object("essay", essay_object)
        essay_resource_uri = json.loads(result.content)['resource_uri']
        essaygrade_object = {'essay' : essay_resource_uri, 'target_scores' : json.dumps([1,1]), 'grader_type' : "IN", 'feedback' : "Was ok.", 'success' : True}
        create_object("essaygrade", essaygrade_object)
    return problem_resource_uri

def lookup_object(resource_uri):
    c = login()
    result = c.get(resource_uri,
                        data={'format' : 'json'}
    )
    return json.loads(result.content)

class GenericTest(object):
    """
    Base class that other model tests inherit from.
    """
    type = "generic"
    object = {'hello' : 'world'}

    def generic_setup(self):
        """
        Setup function that runs tasks common to all modules
        """
        run_setup()
        self.c = login()
        self.endpoint, self.schema = get_urls(self.type)

    def test_schema(self):
        """
        See if the schema can be downloaded
        """
        result = self.c.get(self.schema,
                            data={'format' : 'json'}
        )

        self.assertEqual(result.status_code,200)

    def test_endpoint(self):
        """
        See if the GET method can be used with the endpoint
        """
        result = self.c.get(self.endpoint,
                            data={'format' : 'json'}
        )

        self.assertEqual(result.status_code,200)

    def test_create(self):
        """
        See if POST can be used with the endpoint
        """
        result = self.c.post(self.endpoint, json.dumps(self.object), "application/json")
        self.assertEqual(result.status_code,201)

    def test_update(self):
        """
        See if an object can be created and then updated
        """
        object = model_registry[self.type]()
        result = self.c.put(object, json.dumps(self.object), "application/json")
        self.assertEqual(result.status_code,202)

    def test_delete(self):
        """
        See if an object can be created and then deleted
        """
        object = model_registry[self.type]()
        result = self.c.delete(object)
        self.assertEqual(result.status_code,204)

    def test_view_single(self):
        """
        See if the detail view works for an object
        """
        object = model_registry[self.type]()
        result = self.c.get(object,
                            data={'format' : 'json'}
        )
        self.assertEqual(result.status_code,200)

    def test_search(self):
        """
        Test if we can search in a given endpoint
        """
        object = model_registry[self.type]()
        result = self.c.get(self.endpoint + "search/",
                            data={'format' : 'json'}
        )
        self.assertEqual(result.status_code,200)

class OrganizationTest(unittest.TestCase, GenericTest):
    type="organization"
    object = {"name" : "edX"}

    def setUp(self):
        self.generic_setup()

class CourseTest(unittest.TestCase, GenericTest):
    type="course"
    object = {'course_name' : "edx_test"}
    def setUp(self):
        self.generic_setup()

class ProblemTest(unittest.TestCase, GenericTest):
    type="problem"

    def setUp(self):
        self.generic_setup()
        self.create_object()

    def create_object(self):
        course_resource_uri = create_course()
        self.object = {'courses' : [course_resource_uri], 'max_target_scores' : json.dumps([1,1])}

class EssayTest(unittest.TestCase, GenericTest):
    type="essay"
    def setUp(self):
        self.generic_setup()
        self.create_object()

    def create_object(self):
        problem_resource_uri = create_problem()
        self.object = {'problem' : problem_resource_uri, 'essay_text' : "This is a test essay!", 'essay_type' : 'train'}

class EssayGradeTest(unittest.TestCase, GenericTest):
    type="essaygrade"
    def setUp(self):
        self.generic_setup()
        self.create_object()

    def create_object(self):
        essay_resource_uri = create_essay()
        self.object = {'essay' : essay_resource_uri, 'target_scores' : json.dumps([1,1]), 'grader_type' : "IN", 'feedback' : "Was ok.", 'success' : True}

class MLModelCreationTest(unittest.TestCase):
    def test_ml_creation(self):
        problem_resource_uri = create_ml_essays("train",10)
        problem = lookup_object(problem_resource_uri)
        problem_id = problem['id']
        problem_model = Problem.objects.get(id=problem_id)
        ml_model_creation.handle_single_problem(problem_model)

class FinalTest(unittest.TestCase):
    def test_delete(self):
        """
        Test to see if we can delete all models properly.
        """
        c = login()
        delete_all()
        endpoint, schema = get_urls("organization")
        data = c.get(endpoint, data={'format' : 'json'})
        self.assertEqual(len(json.loads(data.content)['objects']),0)

        endpoint, schema = get_urls("essaygrade")
        data = c.get(endpoint, data={'format' : 'json'})
        self.assertEqual(len(json.loads(data.content)['objects']),0)




