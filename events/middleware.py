import requests
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed,Throttled
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import PermissionDenied
import traceback
from events.api.customexceptions import InvalidUsage

def is_registered(exception):
    try:
        return exception.is_an_error_response
    except AttributeError:
        return False

class AuthGateway(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        url = settings.AUTH_API_GATEWAY_URL + 'users'
        headers = {'Accept': 'application/json;version=1.0', 'Accept-Language': 'en',
        'Authorization': request.META.get('HTTP_AUTHORIZATION')}
        
        res = requests.get(url, headers=headers, timeout=5)
        content = res.json()
        status_code = res.status_code
        
        if status_code == 200:
            request.auth_user = content['data']
        
        elif status_code == 401:
            request.auth_user = {'id': 1}
            #raise PermissionDenied()
            #raise InvalidUsage("Bad Request! Data is poorly formatted")        
        
        response = self.get_response(request)

        return response

    '''
    def process_exception(self, request, exception):
        if is_registered(exception):
            status = exception.status_code
            exception_dict = exception.to_dict()
        else:
            status = 500
            exception_dict = {'errorMessage': 'Unexpected Error!'}
        
        error_message = exception_dict['errorMessage']
        traceback.print_exc()
        return JsonResponse(exception_dict, status=status)
    '''
    
    
        

