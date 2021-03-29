from mooring import models
import ipaddress

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    print (ip)
    return ip


def api_allow(clientip,apikey):
    allow = False
    if models.API.objects.filter(api_key=apikey,active=1).count() > 0:
        api = models.API.objects.filter(api_key=apikey)[0]
        allowed_ips = api.allowed_ips.splitlines()
        for line in allowed_ips:
            if ipaddress.ip_address(clientip) in ipaddress.ip_network(line):
                allow = True

    return allow
