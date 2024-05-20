import requests
from requests_kerberos import HTTPKerberosAuth
import json
import pandas
import urllib3

headers = {'Content-type': 'application/json'}
# Replace the ID here with some article ID
# url = 'https://hsdes-api.intel.com/rest/article/2202652508'
url = 'https://hsdes-api.intel.com/rest/similarity/query/sighting_central/sighting/elastic?verbose=false'
data = '{ "configValue" : "ardenrand:  errors parsing the config file arden_00_socket0_peg.cfg" }'
response = json.loads(requests.post(url, auth=HTTPKerberosAuth(), verify=False, headers=headers, data=data).text)

# print(response)
# Pretty Printing JSON string back
# print(json.dumps(response, indent=4, sort_keys=True))
# print(response['data'][0]['id'], ", ", response['data'][0]['title'])
# for element in response['data']:
#     print("=============================================================")
#     print(element['id'], ", ", element['data'][0]['title'], )
#     print("=============================================================")

# print(pandas.DataFrame(response))