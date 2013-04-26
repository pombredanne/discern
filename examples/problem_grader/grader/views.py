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
import rubric_functions

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

    rubric = {'options' : []}
    if action=="post" and model=="problem":
        rubric = data['rubric'].copy()
        data['max_target_scores'] = [1 for i in xrange(0,len(data['rubric']['options']))]
        del data['rubric']

    slumber_models = setup_slumber_models(user)
    log.debug(slumber_models['problem'].required_fields)

    if model not in slumber_models:
        error = "Invalid model specified :{0} .  Model does not appear to exist in list: {1}".format(model, slumber_models.keys())
        log.info(error)
        raise Exception(error)

    slumber_data = slumber_models[model].action(action,id=id,data=data)
    if action=="post" and model=="problem":
        problem_id = slumber_data['id']
        rubric['problem_id'] = problem_id
        rubric_functions.create_rubric_objects(rubric, request)

    if action in ["get", "post"] and model=="problem":
        if isinstance(slumber_data,list):
            for i in xrange(0,len(slumber_data)):
                rubric_data = rubric_functions.get_rubric_data(slumber_data[i]['id'])
                slumber_data[i]['rubric'] = rubric_data
        else:
            rubric_data = rubric_functions.get_rubric_data(slumber_data['id'])
            slumber_data['rubric'] = rubric_data

    json_data = json.dumps(slumber_data)
    return HttpResponse(json_data)

@login_required
def course(request):
    return render_to_response('course.html', RequestContext(request, {'model' : 'course', 'api_url' : "/grader/action"}))

@login_required
def problem(request):
    if request.method == 'POST':
        args = request.POST
    else:
        args = request.GET

    matching_course_id = args.get('course_id', -1)
    match_course = False
    course_name = None
    if matching_course_id!= -1:
        match_course = True
        user = request.user
        slumber_models = setup_slumber_models(user)
        course_object = slumber_models['course'].action('get',id=matching_course_id, data=None)
        log.debug(course_object)
        course_name = course_object['course_name']

    matching_course_id = str(matching_course_id)


    return render_to_response('problem.html', RequestContext(request, {'model' : 'problem',
                                                                       'api_url' : "/grader/action",
                                                                       'matching_course_id' : matching_course_id,
                                                                       'match_course' : match_course,
                                                                       'course_name' : course_name,
    })
    )

