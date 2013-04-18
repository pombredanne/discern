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

log = logging.getLogger(__name__)

def run_setup():
    if(User.objects.filter(username='test').count() == 0):
        user = User.objects.create_user('test', 'test@test.com', 'test')
        user.save()

def delete_all():
    """
    Teardown function to delete everything in DB
    """
    Organization.objects.all().delete()
    Course.objects.all().delete()
    Problem.objects.all().delete()

def get_urls(resource_name):
    endpoint = reverse("api_dispatch_list", kwargs={'api_name': 'v1','resource_name': resource_name})
    schema = reverse("api_get_schema", kwargs={'api_name': 'v1','resource_name': resource_name})
    return endpoint,schema

def get_first_resource_uri(type):
    c = login()
    endpoint, schema = get_urls(type)
    data = c.get(endpoint, data={'format' : 'json'})
    log.debug(data.content)
    object = json.loads(data.content)['objects'][0]
    resource_uri = [object['resource_uri']]
    return resource_uri

def login():
    c = Client()
    c.login(username='test', password='test')
    return c

class GenericTest(object):
    type = "generic"
    object = {'hello' : 'world'}

    def generic_setup(self):
        run_setup()
        self.c = login()
        self.endpoint, self.schema = get_urls(self.type)

    def test_schema(self):
        result = self.c.get(self.schema,
                            data={'format' : 'json'}
        )

        self.assertEqual(result.status_code,200)

    def test_endpoint(self):
        result = self.c.get(self.endpoint,
                            data={'format' : 'json'}
        )

        self.assertEqual(result.status_code,200)

    def test_create(self):
        result = self.c.post(self.endpoint, json.dumps(self.object), "application/json")
        self.assertEqual(result.status_code,201)


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
        course_resource_uri = get_first_resource_uri("course")
        self.object = {'courses' : course_resource_uri}

class EssayTest(unittest.TestCase, GenericTest):
    type="essay"
    def setUp(self):
        self.generic_setup()
        self.create_object()

    def create_object(self):
        problem_resource_uri = get_first_resource_uri("problem")
        self.object = {'problem' : problem_resource_uri}

class EssayGradeTest(unittest.TestCase, GenericTest):
    type="essaygrade"
    def setUp(self):
        self.generic_setup()


