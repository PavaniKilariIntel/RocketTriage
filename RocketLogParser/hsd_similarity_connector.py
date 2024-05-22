import requests
from requests_kerberos import HTTPKerberosAuth
import sys
import urllib3

headers = {'Content-type': 'application/json'}
hsd_base_url = 'https://hsdes.intel.com/appstore/article/#/'
similarity_url = 'https://hsdes-api.intel.com/rest/similarity/query/sighting_central/sighting/elastic?verbose=false'
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_similar_hsds(config_value):
    payload = '{ "configValue" :  "' + config_value + '" }'
    print("\n\nChecking HSDs for ", config_value)
    response = requests.post(similarity_url, auth=HTTPKerberosAuth(), verify=False, headers=headers, data=payload).json()
    similar_hsds = list()
    for article in response['data']:
        # similar_hsds.append(article["id"])
        if article['status'] != "rejected":
            similar_hsds.append(hsd_base_url+article["id"])
        else:
            print("Ignoring rejected solution : ", article["id"])
        print(f'{hsd_base_url}{article["id"]} {article["title"]}')
    return similar_hsds


def main():
    get_similar_hsds("SAMPLE")


if __name__ == "__main__":
    sys.exit(main())