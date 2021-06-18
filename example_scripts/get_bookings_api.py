import requests

#api_key='5WEEW0D4Q9I7K0XN2Y2Y83RE45HJ66BLYSQ5ZBU866W9CZ3SPY4IPZJQHU0AKQQD6GSG6Z069QOAACFVPBF2SYFOXGZJIOOC301W'
api_key='5G9BIPB17RS7A4WCG33CWAFXI1P39S93BPN61YMZTZV17F6D86XUX9QRDW7ICXQB8A0M1MQM8A92YWC79ZDTPGOKSO0IXIIREMR4'
#url = 'http://172.17.0.3:9007/api/external/bookings/'+api_key+'/'
url = 'https://mooring-api-dev-oim01.dbca.wa.gov.au/api/external/vessel-create-update/'+api_key+'/'
#myobj = {'rego_no': 'D8888','vessel_size': 1.1, 'vessel_draft': 1.2, 'vessel_beam': 1.3, 'vessel_weight' : '1.4',}
myobj = {'date': '2019-09-09', 'rego_no': '112','mooring_id': 46}
x = requests.post(url, data = myobj)
print (x.text)
