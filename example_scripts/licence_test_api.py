import requests

#status = cancelled, active
#licence_type =  1=Licence  2=Authorised User  3=Annual Admission

#api_key='5WEEW0D4Q9I7K0XN2Y2Y83RE45HJ66BLYSQ5ZBU866W9CZ3SPY4IPZJQHU0AKQQD6GSG6Z069QOAACFVPBF2SYFOXGZJIOOC301W'
api_key='5G9BIPB17RS7A4WCG33CWAFXI1P39S93BPN61YMZTZV17F6D86XUX9QRDW7ICXQB8A0M1MQM8A92YWC79ZDTPGOKSO0IXIIREMR4'
url = 'https://mooring-api-dev-oim01.dbca.wa.gov.au/api/external/licence-create-update/'+api_key+'/'
myobj = {'vessel_rego': 'D8888','licence_id': 1235, 'licence_type': 2, 'start_date': '2021-08-21','expiry_date' : '2022-05-20', 'status' : 'active'}
resp = requests.post(url, data = myobj)
print (resp.text)
