from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from slumber_models import SlumberModelDiscovery
from django.conf import settings
from django.contrib.auth.decorators import login_required
import logging
import json

log = logging.getLogger(__name__)

def setup_slumber_models(user, model_types=None):
    api_auth = user.profile.get_api_auth()
    slumber_discovery = SlumberModelDiscovery(settings.FULL_API_START, api_auth)
    models = slumber_discovery.generate_models(model_types)
    return models

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/grader/")
    else:
        form = UserCreationForm()
    return render_to_response("registration/register.html", RequestContext(request,{
        'form': form,
        }))

def index(request):
    return render_to_response("index.html",RequestContext(request))

action_types = ["update", "delete", "get", "post"]

@login_required
def action(request):
    if request.method == 'POST':
        args = request.POST
    else:
        args = request.GET

    action = args.get('action', 'get')
    model = args.get('model', None)
    id = args.get('id', None)

    user = request.user
    data = args.get('data', None)

    try:
        data = json.loads(data)
    except:
        pass

    if action is None or action not in action_types:
        error = "Action cannot be None, and must be a string in action_types: {0}".format(action_types)
        log.info(error)
        raise TypeError(error)

    slumber_models = setup_slumber_models(user)

    if model not in slumber_models:
        error = "Invalid model specified :{0} .  Model does not appear to exist in list: {1}".format(model, slumber_models.keys())
        log.info(error)
        raise Exception(error)
    json_data = json.dumps(slumber_models[model].action(action,id=id,data=data))
    return HttpResponse(json_data)

@login_required
def course(request):
    return render_to_response('course.html', RequestContext(request, {'model' : 'course', 'api_url' : "/grader/action"}))

def problem(request):
    if request.method == 'POST':
        args = request.POST
    else:
        args = request.GET

    matching_course_id = args.get('course_id', -1)
    match_course = False
    if matching_course_id!= -1:
        match_course = True

    return render_to_response('problem.html', RequestContext(request, {'model' : 'problem', 'api_url' : "/grader/action", 'course_id' : matching_course_id, 'match_course' : match_course}))

