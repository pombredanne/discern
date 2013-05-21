==================================
Usage
==================================

This page walks you through lauching discern and exploring its APIs. Before we begin, let's sanity check for ease module installation. Simply import the ease.grade module. 
::
	$ python manage.py shell 
	Python 2.7.3 (default, Aug  1 2012, 05:16:07) 
	[GCC 4.6.3] on linux2
	Type "help", "copyright", "credits" or "license" for more information.
	(InteractiveConsole)
	>>> import ease.grade
	>>> 

On success, it should simply return you to the python prompt. If it throws an exception, there is a problem with the ease installation. 

Now let's run discern. You will need to run both the API server and the celery backend to process tasks.

1. ``python manage.py runserver 127.0.0.1:7999 --nostatic --settings=discern.settings --pythonpath=. &``
2. ``python manage.py celeryd -B --settings=discern.settings --pythonpath=. --loglevel=debug --logfile=/tmp/celery$$.out &``

Admin Interface
------------------------------
There is an easy to use frontend for Admin Interface.  In order to use it, just navigate to 127.0.0.1:7999.  After that, you will be able to register using the links at the top.  After you register, you will see links to the API models.  Each model will allow you to get a list of existing models, add new ones, delete existing ones, and update them.  See the :ref:`api_models` section for more details on the models.

Getting started - the plan
------------------------------

Discern allows anyone to use machine learning based automated textual classification as an API service. You would generally want text that is associated with one or more *scores*. These *scores* can be anything. One example would be a corpus of essays that are scored. Another example would be `reddit <http://www.reddit.com/>`_ comments/posts, which are associated with upvotes/downvotes, which are a *score*. Another example would be news articles and stock prices before/after the news articles were released.

We will use the python `Request module <http://docs.python-requests.org/en/latest/>`_ to interact with our Discern server. For our examples,the response will be in `JSON <http://en.wikipedia.org/wiki/JSON>`_. The example code is broken down into small programs(e.g., to login, to create a user, etc). Each will include this python module. 

.. literalinclude:: ../examples/common_settings.py
   :language: python
   :linenos:

The basic outline for this tutorial is:

#. Becoming familiar with the API and logging into Discern. 
#. Created an organization object, a course object, and a problem object.
#. Associate the course with the organization and the problem with the course.
#. Add 10 essay objects and associate them with the problem.
#. Add 10 essay grade objects that are instructor scored and associate each one with an essay.
#. A model will now be created, and from now on, each additional essay you add will automatically have an essay grade object associated with it that contains the machine score.

Getting started - becoming familiar with the API
--------------------------------------------------

As configured in this tutorial, the main end point for discern is `http://127.0.0.1:7999/essay_site/api/v1`. 
Consider the following code segment which enumerates the endpoints offered by Discern.

.. literalinclude:: ../examples/connect_to_api.py
   :language: python
   :linenos:

and here is the resulting output.
::
	$ python connect_to_api.py 
	Status Code: 200
	{u'essay': {u'list_endpoint': u'/essay_site/api/v1/essay/', u'schema': u'/essay_site/api/v1/essay/schema/'}, u'essaygrade': {u'list_endpoint': u'/essay_site/api/v1/essaygrade/', u'schema': u'/essay_site/api/v1/essaygrade/schema/'}, u'course': {u'list_endpoint': u'/essay_site/api/v1/course/', u'schema': u'/essay_site/api/v1/course/schema/'}, u'membership': {u'list_endpoint': u'/essay_site/api/v1/membership/', u'schema': u'/essay_site/api/v1/membership/schema/'}, u'user': {u'list_endpoint': u'/essay_site/api/v1/user/', u'schema': u'/essay_site/api/v1/user/schema/'}, u'createuser': {u'list_endpoint': u'/essay_site/api/v1/createuser/', u'schema': u'/essay_site/api/v1/createuser/schema/'}, u'organization': {u'list_endpoint': u'/essay_site/api/v1/organization/', u'schema': u'/essay_site/api/v1/organization/schema/'}, u'problem': {u'list_endpoint': u'/essay_site/api/v1/problem/', u'schema': u'/essay_site/api/v1/problem/schema/'}, u'userprofile': {u'list_endpoint': u'/essay_site/api/v1/userprofile/', u'schema': u'/essay_site/api/v1/userprofile/schema/'}}
	Model: essay Endpoint: /essay_site/api/v1/essay/ Schema: /essay_site/api/v1/essay/schema/
	Model: essaygrade Endpoint: /essay_site/api/v1/essaygrade/ Schema: /essay_site/api/v1/essaygrade/schema/
	Model: course Endpoint: /essay_site/api/v1/course/ Schema: /essay_site/api/v1/course/schema/
	Model: membership Endpoint: /essay_site/api/v1/membership/ Schema: /essay_site/api/v1/membership/schema/
	Model: user Endpoint: /essay_site/api/v1/user/ Schema: /essay_site/api/v1/user/schema/
	Model: createuser Endpoint: /essay_site/api/v1/createuser/ Schema: /essay_site/api/v1/createuser/schema/
	Model: organization Endpoint: /essay_site/api/v1/organization/ Schema: /essay_site/api/v1/organization/schema/
	Model: problem Endpoint: /essay_site/api/v1/problem/ Schema: /essay_site/api/v1/problem/schema/
	Model: userprofile Endpoint: /essay_site/api/v1/userprofile/ Schema: /essay_site/api/v1/userprofile/schema/
	Status Code: 401


The last status code from the output was 401 because we aren't logged in. To proceed, we will have to create a user. Here is the code to create a user called *test*. Let's create one. 

.. literalinclude:: ../examples/create_user.py
   :language: python
   :linenos:

Alternatively, if you want a UI to interactively play around with these APIs, the POSTMAN add-on for Chrome is highly recommended. The endpoint is http://127.0.0.1:7999/essay_site/api/v1/createuser/. Just POST a JSON data dictionary containing the keys username and password (i.e., *{"username" : "test", "password" : "test"}* ).

Getting started - creating objects 
---------------------------------------

At this point, you'll want to create an organization object, a course object, and a problem object. To allow us to focus on the Discern API, we will use reddit.  
