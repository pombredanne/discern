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
        data.update({
            'premium_feedback_models' : "",
            'number_of_additional_predictors' : 0,
            'max_target_scores' : [1 for i in xrange(0,len(data['rubric']['options']))],
            'courses' : ["/" + settings.API_URL_INTERMEDIATE + "course/" + str(data['course']) + "/"]
        })
        del data['rubric']
        del data['course']

    if action=="post" and model=="essay":
        data['problem'] = "/" + settings.API_URL_INTERMEDIATE + "problem/" + str(data['problem']) + "/"

    slumber_models = setup_slumber_models(user)
    log.debug(slumber_models['essay'].required_fields)

    if model not in slumber_models:
        error = "Invalid model specified :{0} .  Model does not appear to exist in list: {1}".format(model, slumber_models.keys())
        log.info(error)
        raise Exception(error)

    try:
        slumber_data = slumber_models[model].action(action,id=id,data=data)
    except Exception as inst:
        log.debug(inst.args)
        log.debug(inst.response)
        log.debug(inst.content)
        raise

    log.debug(slumber_models['essaygrade'].required_fields)

    if action=="post" and model=="problem":
        problem_id = slumber_data['id']
        rubric['problem_id'] = problem_id
        rubric_functions.create_rubric_objects(rubric, request)

    #Append rubric to problem and essay objects
    if (action in ["get", "post"] and model=="problem") or (action=="get" and model=="essay"):
        if isinstance(slumber_data,list):
            for i in xrange(0,len(slumber_data)):
                try:
                    if model=="problem":
                        problem_id = slumber_data[i]['id']
                    else:
                        problem_id = slumber_data[i]['problem'].split('/')[5]

                    rubric_data = rubric_functions.get_rubric_data(problem_id)
                    slumber_data[i]['rubric'] = rubric_data
                except:
                    log.error("Could not find rubric for problem id {0}.".format(problem_id))
                    slumber_data[i]['rubric'] = []
        else:
            rubric_data = rubric_functions.get_rubric_data(slumber_data['id'])
            slumber_data['rubric'] = rubric_data

    #append essaygrades to essay objects
    if action=="get" and model=="essay":
        essaygrades = slumber_models['essaygrade'].action('get')
        if isinstance(slumber_data,list):
            for i in xrange(0,len(slumber_data)):
                slumber_data[i]['essaygrades_full'] = get_essaygrade_data(slumber_data[i], essaygrades)
        else:
            slumber_data['essaygrades_full'] = get_essaygrade_data(slumber_data, essaygrades)

    json_data = json.dumps(slumber_data)
    return HttpResponse(json_data)

def get_essaygrade_data(slumber_data, essaygrades):
    problem_id = slumber_data['problem'].split('/')[5]
    essaygrade_data = []
    for z in xrange(0,len(slumber_data['essaygrades'])):
        essaygrade_id = slumber_data['essaygrades'][z].split('/')[5]
        for i in xrange(0,len(essaygrades)):
            if int(essaygrade_id) == int(essaygrades[i]['id']):
                target_scores = essaygrades[i]['target_scores']
                try:
                    target_scores = json.loads(target_scores)
                except:
                    pass
                rubric_data = rubric_functions.get_rubric_data(problem_id, target_scores)
                essaygrades[i]['rubric'] = rubric_data
                essaygrade_data.append(essaygrades[i])
    return essaygrade_data

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

@login_required
def write_essays(request):
    return render_to_response('write_essay.html', RequestContext(request, {'api_url' : "/grader/action", 'model' : 'essay',}))

@login_required
def grade_essays(request):
    return render_to_response('grade_essay.html', RequestContext(request, {'api_url' : "/grader/action", 'model' : 'essaygrade',}))


