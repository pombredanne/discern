import rubric_functions
import json
import logging
from django.conf import settings
from slumber_models import SlumberModelDiscovery

log=logging.getLogger(__name__)

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