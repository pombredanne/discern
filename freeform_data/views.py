from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse
import logging

log=logging.getLogger(__name__)

@csrf_exempt
def login(request):
    """
    Handles external login request.
    """
    if request.method != 'POST':
        return error_response('Must query using HTTP POST.')

    p = request.POST.copy()
    try:
        p = json.loads(p)
    except:
        pass

    log.debug(p)
    log.debug(request)

    if not p.has_key('username') or not p.has_key('password'):
        return error_response('Insufficient login info')

    user = authenticate(username=p['username'], password=p['password'])
    if user is not None:
        login(request, user)
        return success_response('Logged in.')
    else:
        return error_response('Incorrect login credentials.')

def logout(request):
    """
    Uses django auth to handle a logout request
    """
    logout(request)
    return success_response('Goodbye')

def success_response(message):
    return generic_response(message, True)

def error_response(message):
    return generic_response(message, False)

def generic_response(message, success):
    message = {'success' : success, 'message' : message}
    return HttpResponse(json.dumps(message))