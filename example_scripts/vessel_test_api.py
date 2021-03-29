import requests

api_key='5WEEW0D4Q9I7K0XN2Y2Y83RE45HJ66BLYSQ5ZBU866W9CZ3SPY4IPZJQHU0AKQQD6GSG6Z069QOAACFVPBF2SYFOXGZJIOOC301W'

#url = 'http://172.17.0.3:9002//api/external/all-mooring/'+api_key+'/?mooring_specification=private'
url = 'http://172.17.0.3:9002/api/external/vessel-create-update/'+api_key+'/'
myobj = {'rego_no': 'D8888','vessel_size': 1.1, 'vessel_draft': 1.2, 'vessel_beam': 1.3, 'vessel_weight' : '1.4',}
x = requests.post(url, data = myobj)
print (x.text)
