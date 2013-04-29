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
    """
    Sets up the slumber API models for a given user.  See slumber_models for a description of slumber
    user - a django user object
    model_types - if you only want to setup certain types of models, pass them in
    """
    #Get the api authentication dictionary for the user
    api_auth = user.profile.get_api_auth()
    #Instantiate the slumber model discovery class for the api endpoint specified in settings
    slumber_discovery = SlumberModelDiscovery(settings.FULL_API_START, api_auth)
    #Generate all the models
    models = slumber_discovery.generate_models(model_types)
    return models

def register(request):
    """
    Register a new user for a given request
    """
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
    """
    Index page for the site.
    """
    return render_to_response("index.html",RequestContext(request))

#Available types of actions
action_types = ["update", "delete", "get", "post"]

@login_required
def action(request):
    """
    Main handler function for actions.  Needs to be broken up down the line.
    """

    #Support get or post requests
    if request.method == 'POST':
        args = request.POST
    else:
        args = request.GET

    #Action is the type of action to do (see action_types above)
    action = args.get('action', 'get')
    #Model is the model to perform the given action on(ie 'organization')
    model = args.get('model', None)
    #If the action is on a per-instance level (ie delete and update), then get the id to perform the action on.
    id = args.get('id', None)

    #Grab the user
    user = request.user
    #Data is used when posting and updating
    data = args.get('data', None)

    #Data might be in json format, but it might not.  support both
    try:
        data = json.loads(data)
    except:
        pass

    #Check to see if the action is valid.
    if action is None or action not in action_types:
        error = "Action cannot be None, and must be a string in action_types: {0}".format(action_types)
        log.info(error)
        raise TypeError(error)

    #Define a base rubric
    rubric = {'options' : []}
    #If we are posting a problem, then there is additional processing to do before we can submit to the API
    if action=="post" and model=="problem":
        #Grab the rubric for later.
        rubric = data['rubric'].copy()
        #Add in two needed fields (the api requires them)
        data.update({
            'max_target_scores' : [1 for i in xrange(0,len(data['rubric']['options']))],
            'courses' : [construct_related_uri(data['course'], 'course')]
        })
        #Remove these keys (posting to the api will fail if they are still in)
        del data['rubric']
        del data['course']

    #We need to convert the integer id into a resource uri before posting to the API
    if action=="post" and model=="essay":
        data['problem'] = construct_related_uri(data['problem'], 'problem')

    #We need to convert the integer id into a resource uri before posting to the API
    if action=="post" and model=="essaygrade":
        data['essay'] = construct_related_uri(data['essay'], 'essay')

    #If we are deleting a problem, delete its local model uri
    if action=="delete" and model=="problem":
        rubric_functions.delete_rubric_data(id)

    #Setup all slumber models for the current user
    slumber_models = setup_slumber_models(user)

    #Check to see if the user requested model exists at the API endpoint
    if model not in slumber_models:
        error = "Invalid model specified :{0} .  Model does not appear to exist in list: {1}".format(model, slumber_models.keys())
        log.info(error)
        raise Exception(error)

    try:
        #Try to see if we can perform the given action on the given model
        slumber_data = slumber_models[model].action(action,id=id,data=data)
    except Exception as inst:
        #If we cannot, log the error information from slumber.  Will likely contain the error message recieved from the api
        error_message = "Could not perform action {action} on model type {model} with id {id} and data {data}.".format(action=action, model_type=model, id=id, data=data)
        error_information = "Recieved the following from the server.  Args: {args} , response: {response}, content: {content}".format(args=inst.args, response=inst.response, content=inst.content)
        log.error(error_message)
        log.error(error_information)
        raise

    #If we have posted a problem, we need to create a local rubric object to store our rubric (the api does not do this)
    if action=="post" and model=="problem":
        problem_id = slumber_data['id']
        rubric['problem_id'] = problem_id
        #Create the rubric object
        rubric_functions.create_rubric_objects(rubric, request)

    #Append rubric to problem and essay objects
    if (action in ["get", "post"] and model=="problem") or (action=="get" and model=="essay"):
        if isinstance(slumber_data,list):
            for i in xrange(0,len(slumber_data)):
                    slumber_data[i]['rubric'] = get_rubric_data(model, slumber_data[i])
        else:
            slumber_data['rubric'] = get_rubric_data(model, slumber_data)

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

def get_rubric_data(model, slumber_data):
    if model=="problem":
        problem_id = slumber_data['id']
    else:
        problem_id = slumber_data['problem'].split('/')[5]

    rubric_data = []
    try:
        rubric_data = rubric_functions.get_rubric_data(problem_id)
    except:
        log.error("Could not find rubric for problem id {0}.".format(problem_id))

    return rubric_data

def construct_related_uri(id, model_type):
    return "/{api_url}{model_type}/{id}/".format(api_url=settings.API_URL_INTERMEDIATE, model_type=model_type, id=id)

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


