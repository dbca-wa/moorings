from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from mooring import models
from mooring import common_iplookup 
from django.db.models import Q
import json
import ipaddress

def create_vessel(request, apikey):
    ledger_json = {}
    jsondata = {'status': 404, 'message': 'API Key Not Found'}

    if models.API.objects.filter(api_key=apikey,active=1).count():
        if common_iplookup.api_allow(common.get_client_ip(request),apikey) is True:

            jsondata['status'] = 200
            jsondata['message'] = 'Groups Retreived'

        else:
            jsondata['status'] = 403
            jsondata['message'] = 'Access Forbidden'

    return HttpResponse(json.dumps(jsondata), content_type='application/json')

