import requests
from django.conf import settings
from rest_framework.exceptions import NotAuthenticated
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response



class LoginRequiredMixin(object):
    url = settings.AUTH_API_GATEWAY_URL + 'users'

    def dispatch(self, request, *args, **kwargs):
        headers = {'Accept': 'application/json;version=1.0', 'Accept-Language': 'en',
        'Authorization': request.META.get('HTTP_AUTHORIZATION')}

        res = requests.get(self.url, headers=headers, timeout=5)
        content = res.json()
        status_code = res.status_code
        if status_code == 200:
            request.auth_user = content['data']
            
            return Response(['fkdjkf'])
        
        else:
            raise NotAuthenticated