import requests

api_key='<api_key>'
#url = 'http://172.17.0.3:9002//api/external/all-mooring/'+api_key+'/?mooring_specification=private'
url = 'https://mooring-api-dev-oim01.dbca.wa.gov.au/api/external/vessel-create-update/'+api_key+'/'
myobj = {'rego_no': 'D8888','vessel_size': 1.1, 'vessel_draft': 1.2, 'vessel_beam': 1.3, 'vessel_weight' : '1.4',}
x = requests.post(url, data = myobj)
print (x.text)
