import requests
from requests_kerberos import HTTPKerberosAuth
import hsd_summarizer as hsd
import sys
import urllib3

headers = {'Content-type': 'application/json'}
hsd_base_url = 'https://hsdes.intel.com/appstore/article/#/'
similarity_url = 'https://hsdes-api.intel.com/rest/similarity/query/sighting_central/sighting/elastic?verbose=false'
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
openai_conn = hsd.get_openai_connector()


def summarize_hsd(full_hsd_info):
    prompt = f"Please sumarize the text below which describes a failure observed in a system. Try to figure out if a solution was found. Do not expand acronyms. The text includes a title, a description and a series of cronological comments or updates.\n\n{full_hsd_info}"

    # messages to be sent to the OpenAI model
    messages = [
        {"role": "user", "content": prompt}
    ]

    # openai_conn = hsd.get_openai_connector()
    res = openai_conn.run_prompt(messages)
    print("OPEN AI RESPONSE :: ", str(res['response']))
    return res['response']


def get_similar_hsds(config_value):
    payload = '{ "configValue" :  "' + config_value + '" }'
    print("\n\nChecking HSDs for ", config_value)
    response = requests.post(similarity_url, auth=HTTPKerberosAuth(), verify=False, headers=headers, data=payload).json()
    similar_hsds = list()
    for article in response['data']:
        # similar_hsds.append(article["id"])
        if article['status'] != "rejected":
            current_hsd = hsd_base_url+article["id"]
            hsd_summary = summarize_hsd(hsd.fetch_full_hsd_data(article["id"]))
            # hsd_summary = article["id"]
            # print("-=-=-=-=-=--=-=-==-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
            # print("-=-=-=-=-=--=-=-==-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
            # print(hsd_summary)
            # print("-=-=-=-=-=--=-=-==-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
            # print("-=-=-=-=-=--=-=-==-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
            similar_hsds.append(current_hsd + " ::: " + str(hsd_summary))
        else:
            print("Ignoring rejected solution : ", article["id"])
        print(f'{hsd_base_url}{article["id"]} {article["title"]}')
    return similar_hsds


def main():
    get_similar_hsds("SAMPLE")


if __name__ == "__main__":
    sys.exit(main())