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

class GenericTest(object):
    type = "generic"

    def generic_setup(self):
        run_setup()
        self.c = Client()
        self.c.login(username='test', password='test')
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


class OrganizationTest(unittest.TestCase, GenericTest):
    type="organization"
    def setUp(self):
        self.generic_setup()

class CourseTest(unittest.TestCase, GenericTest):
    type="course"
    def setUp(self):
        self.generic_setup()

class ProblemTest(unittest.TestCase, GenericTest):
    type="problem"
    def setUp(self):
        self.generic_setup()

class EssayTest(unittest.TestCase, GenericTest):
    type="essay"
    def setUp(self):
        self.generic_setup()

class EssayGradeTest(unittest.TestCase, GenericTest):
    type="essaygrade"
    def setUp(self):
        self.generic_setup()


