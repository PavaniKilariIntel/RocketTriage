import requests
from requests_kerberos import HTTPKerberosAuth
import json
import pandas
import urllib3


headers = {'Content-type': 'application/json'}
# Replace the ID here with some article ID
# url = 'https://hsdes-api.intel.com/rest/article/2202652508'
hsd_url = 'https://hsdes.intel.com/appstore/article/#/'
url = 'https://hsdes-api.intel.com/rest/similarity/query/sighting_central/sighting/elastic?verbose=false'
payload = '{ "configValue" : "ardenrand:  errors parsing the config file arden_00_socket0_peg.cfg" }'
# response = json.loads(requests.post(url, auth=HTTPKerberosAuth(), verify=False, headers=headers, data=payload).text)
response = requests.post(url, auth=HTTPKerberosAuth(), verify=False, headers=headers, data=payload).json()

#(response)
# Pretty Printing JSON string back
# print(json.dumps(response, indent=4, sort_keys=True))
# print(response['data'][0]['id'], ", ", response['data'][0]['title'])
for article in response['data']:
    print(f'{hsd_url}{article["id"]} {article["title"]}')

# print(pandas.DataFrame(response))