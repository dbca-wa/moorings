import requests

#status = cancelled, active
#licence_type =  1=Licence  2=Authorised User  3=Annual Admission

api_key='<api_key>'
url = 'https://mooring-api-dev-oim01.dbca.wa.gov.au/api/external/licence-create-update/'+api_key+'/'
myobj = {'vessel_rego': 'D8888','licence_id': 1235, 'licence_type': 2, 'start_date': '2021-08-21','expiry_date' : '2022-05-20', 'status' : 'active'}
resp = requests.post(url, data = myobj)
print (resp.text)
