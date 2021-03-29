import requests

#status = cancelled, active
#licence_type =  1=Licence  2=Authorised User  3=Annual Admission

api_key='5WEEW0D4Q9I7K0XN2Y2Y83RE45HJ66BLYSQ5ZBU866W9CZ3SPY4IPZJQHU0AKQQD6GSG6Z069QOAACFVPBF2SYFOXGZJIOOC301W'
url = 'http://172.17.0.3:9002/api/external/licence-create-update/'+api_key+'/'
myobj = {'vessel_rego': 'D8888','licence_id': 1235, 'licence_type': 2, 'start_date': '2021-02-18','expiry_date' : '2022-05-20', 'status' : 'active'}
resp = requests.post(url, data = myobj)
print (resp.text)
