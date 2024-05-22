import os
import traceback
import re
import types
import getpass
from bs4 import BeautifulSoup
import sys

# WARNING
# WARNING   This is not the recommended method. Users should copy the required connectors into the app folder and import locally.
# WARNING   This is not the recommended method. Users should copy the required connectors into the app folder and import locally.
# WARNING   This is not the recommended method. Users should copy the required connectors into the app folder and import locally.
# WARNING
# WARNING   For this demo app I decided not to copy the connectors. I can then use this app
# WARNING   to verify current version of the connectors is still working.
# WARNING

# Add connectors directory to the path to allow for connectors to be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "connectors")))

import send_email_connector as email_connector
from openai_connector import OpenAIConnector
from hsd_connector import HsdConnector

_comment_hsd_summary_title = "This is an AI-generated summary"

#https://hsdes.intel.com/appstore/article/#/22019778024
re_hsd_url = re.compile("^https://hsdes.*intel.com.*/(?P<id>[0-9]{9,15})")
re_hsd_id = re.compile("^(?P<id>[0-9]{9,15})$")
re_comment = re.compile("^\++(?P<comment_id>\d+)\s+(?P<user>[a-z0-9]+)$")
      
hsd_url_template = "https://hsdes.intel.com/appstore/article/#/<ID>"
      
DELIVERY_HTML  = "html"
DELIVERY_EMAIL = "email"
DELIVERY_ALL   = "all"
       
def explode_hsd_ids(intxt):
    hsd_ids = []
    err = False
    intxt = intxt.replace("\n",",")
    for hsd in intxt.split(","):
        hsd = hsd.strip()
        if hsd == "": continue
        m = re_hsd_id.match(hsd)
        if m is not None:
            hsd_ids.append(m.groupdict()["id"])
            continue
        m = re_hsd_url.match(hsd)
        if m is not None:
            hsd_ids.append(m.groupdict()["id"])
            continue
        print("Invalid ID or URL: %s"%(repr(hsd),))
        err = True
    if len(hsd_ids) == 0:
        raise Exception("Did not find any valid HSD ID")
    if err:
        return None
        
    # Remove duplicated entries!
    hsd_ids = list(set(hsd_ids))
    
    return hsd_ids

def _get_user_inputs():
    options = types.SimpleNamespace()
    
    while True:
        intxt = input("Give me one or more comma-separated HSDs to process, either by ID or full URL: ")
        try:
            options.hsd_ids = explode_hsd_ids(intxt)
        except Exception as ex:
            print("ERR: %s"%(ex,))
            options.hsd_ids = None
        if options.hsd_ids is not None:
            break
        print("Try again...")
    
    while True:
        delivery = input("Which delivery method should I use?\n 1) email\n 2) Local HTML document\n 3) all above\n > ")
        if delivery == "1":
            options.delivery = DELIVERY_EMAIL
            break
        if delivery == "2":
            options.delivery = DELIVERY_HTML
            break
        if delivery == "3":
            options.delivery = DELIVERY_ALL
            break
        print("Try agian...")

    if options.delivery in (DELIVERY_ALL, DELIVERY_EMAIL):
        curr_user = getpass.getuser()
        options.email_addresses = input("Please provide one or more comma-separated email recipients.\n  "
                                        "Provide either an Intel IDSD (without domain) or a full email address.\n  >"
                                        "Leave emtpy to email to current user [%s] > "%(curr_user,))
        if options.email_addresses == "":
            options.email_addresses = curr_user
    else:
        options.email_addresses = None

    while True:
        post_comment = input("Should the app insert a new comment on each HSD with the generated summary? [y/n] ")
        if post_comment.lower() in ("y","n"):
            options.post_comment = post_comment.lower() == "y"
            if options.post_comment:
                if input("  \\----> Are you sure? This will insert a new comment in %i HSDs. y/n: "%(len(options.hsd_ids),)) == "y":
                    break
            else:
                break  # n
        print("Try again...")
    
    return options
    
_hsd_connector = None
def get_hsd_connector():
    global _hsd_connector
    if _hsd_connector is None:
        _hsd_connector = HsdConnector()
    return _hsd_connector
    
_openai_connector = None
def get_openai_connector(version = None):
    global _openai_connector
    if _openai_connector is None:
        _openai_connector = OpenAIConnector(version)
    return _openai_connector
    
def fetch_full_hsd_data(hsd_id, 
                        print_report_id = "",
                        status_callback = None, 
                        status_session_id = None,
                        ):
    hsd_data = types.SimpleNamespace()
    hsd_conn = get_hsd_connector()

    data = hsd_conn.get_hsd(hsd_id, ["collaborators","title","comments","description","tenant","subject"])
    assert data is not None, "Failed to fetch HSD info"
    # Some HSDs have empty description and return None
    assert data["description"] is not None, "HSD %s description is empty!"%(hsd_id,)
    
    hsd_data.raw_data = data
        
    print("%sTitle: %s"%(print_report_id, data["title"]))
    
    # hsd_data.full_hsd_info = "Title: %s\n\n"%(data["title"],)
    # hsd_data.full_hsd_info += "Description: %s\n\n"%(BeautifulSoup(data["description"], "html.parser").get_text(separator=" ", strip = True),)
    hsd_data.full_hsd_info = ""
    hsd_data.full_hsd_info += (BeautifulSoup(data["description"], "html.parser").get_text(separator=" ", strip = True))

    # Find comment IDs on the HSD data
    found_comments = []
    hsd_data.comment_data = {}
    if data["comments"] is None:
        print("WARNING: HSD %s does not seem to have any comment inserted yet!"%(hsd_id,))
    else:
        for line in data["comments"].split("\n"):
            m = re_comment.match(line) 
            if m is not None:
                d = m.groupdict()
                found_comments.append(d["comment_id"])
    
    hsd_data.comments_raw_data = {}
    
    kept_comments = []
    for index,comment_id in enumerate(found_comments):
            set_status(callback = status_callback, session_id = status_session_id, 
                status = "%sProcessing comment %s (%i/%i)"%(print_report_id, comment_id, index + 1, len(found_comments)))
        
            comm_data = hsd_conn.get_hsd(comment_id, ["submitted_date", 'submitted_by', "description"])
            hsd_data.comments_raw_data[comment_id] = comm_data
            
            comm_text = BeautifulSoup(comm_data["description"], "html.parser").get_text(separator=" ", strip = True)
            
            if _comment_hsd_summary_title in comm_text:
                print("WARNING: Skipping comment %s since it seems to be a previously-generated AI summary"%(comment_id,))
                continue
            
            kept_comments.append(comment_id)
            
            #print("-"*20)
            #pprint.pprint(comm_data)
            hsd_data.comment_data[comment_id] = "Comment by %s on %s\n%s\n\n"%(
                comm_data["submitted_by"], comm_data["submitted_date"],
                comm_text,)
    
    kept_comments.reverse()
    for comment in kept_comments:
        hsd_data.full_hsd_info += hsd_data.comment_data[comment] + "\n\n"
    
    return hsd_data
    
def build_summary_html(hsds_data):
        
    body = '''<header>
<style>
body {
  font-family: Arial, Helvetica, sans-serif;
  word-wrap: break-word;
  word-break: break-all;
}
#title{
  color:#084;
  font-weight:bold;
}
#warning{
  color:#F40;
  font-weight:bold;
}
#demotable {
  font-family: Arial, Helvetica, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

#demotable td, #demotable th {
  border: 1px solid #ddd;
  padding: 8px;
}

#demotable tr:nth-child(even){background-color: #f2f2f2;}

#demotable tr:hover {background-color: #ddd;}

#demotable th {
  padding-top: 12px;
  padding-bottom: 12px;
  text-align: left;
  background-color: #04AA6D;
  color: white;
}
</style>
<body>
'''
    body += email_connector.html_format_span("OpenAI-generated HSD summaries\n\n", id="title")
    body += '''
<table id="demotable">
  <tr>
    <th>HSD</th>
    <th>Title</th>
    <th>Summary</th>
  </tr>
'''
    for hsd_id, hsd_data in hsds_data.items():
        body += "  <tr>\n"
        body += "    <td><a href=\"%s\" target=\"_BLANK\">%s</a></td>"%(hsd_url_template.replace("<ID>", hsd_id), hsd_id,)
        body += "    <td>%s</td>"%(email_connector.html_escape(hsd_data.title),)
        body += "    <td>%s</td>"%(email_connector.html_escape(hsd_data.summary),)
        body += "  </tr>\n"
    
    body += "  </table>\n"
    body += "</body>"
    
    return body
      
def set_status(status, callback = None, session_id = None):
    print(status + "        \r", flush=True, end="")
    if callback is not None:
        callback(session_id, status)
      
def process_hsds(hsd_ids, 
                 delivery, 
                 post_comment = False, 
                 html_output = "summary.html", 
                 email_addresses = None, 
                 status_callback = None, 
                 status_session_id = None,
                 open_html = True):
    if type(hsd_ids) == str:
        hsd_ids = explode_hsd_ids(hsd_ids)
        assert hsd_ids is not None, "Received Invalid HSD IDs"
    
    assert delivery in (DELIVERY_HTML, DELIVERY_EMAIL, DELIVERY_ALL), "Invalid delivery: %s"%(repr(delivery),)
    assert delivery not in (DELIVERY_EMAIL, DELIVERY_ALL) or email_addresses is not None, "email_addresses is required for email delivery"

    hsds_data = {}

    for index, hsd_id in enumerate(hsd_ids):
        hsds_data[hsd_id] = types.SimpleNamespace()
        hsds_data[hsd_id].title = "N/A"
        
        report_id = "HSD %s (%i/%i) - "%(hsd_id, index + 1, len(hsd_ids))
        try:
            # Get HSD data
            set_status(callback = status_callback, session_id = status_session_id, status = "%sFetching HSD data"%report_id)
                
            hsd_data = fetch_full_hsd_data(hsd_id, print_report_id = report_id, status_callback = status_callback, status_session_id = status_session_id)
            hsds_data[hsd_id].data = hsd_data
            hsds_data[hsd_id].title = hsd_data.raw_data["title"]
                
            prompt=f"Please sumarize the text below which describes a failure observed in a system. Try to figure out if a solution was found. Do not expand acronyms. The text includes a title, a description and a series of cronological comments or updates.\n\n{hsd_data.full_hsd_info}"
            
            # messages to be sent to the OpenAI model
            messages = [
                {"role": "user", "content": prompt}
            ]
            
            set_status(callback = status_callback, session_id = status_session_id, status = "%sRunning openAI summary query"%(report_id,))
            
            openai_conn = get_openai_connector()
            res = openai_conn.run_prompt(messages)
            
            # print the response
            print("\n\nResult (HSD %s summary):\n%s\n%s\n%s"%(hsd_id, "-"*80, res["response"], "-"*80))
            hsds_data[hsd_id].summary = res["response"]
            
        except BaseException as ex:
            hsds_data[hsd_id].summary = "Failed to process HSD\n%s"%(ex,)
            print("%sERROR: Caught exception processig HSD: %s"%(report_id, ex))
            print(traceback.format_exc())
            continue
        
        try:
            if post_comment:
                set_status(callback = status_callback, session_id = status_session_id, status = "%sPosting comment update"%(report_id,))
                
                summary = "WARNING: %s using %s.\n\n%s"%(_comment_hsd_summary_title, os.path.basename(__file__), res["response"],)
                summary = summary.replace("\n","<br/>")
                
                new_id = get_hsd_connector().set_comment(tenant = hsd_data.raw_data["tenant"], 
                                                         parent_id = hsd_id, 
                                                         description = summary, 
                                                         send_mail = True)
            
                print("%sHSD summary inserted as a new comment with id %i"%(report_id, new_id,))
        except BaseException as ex:
            print("%sERROR: Caught exception posting comment for HSD: %s"%(report_id, ex))
            print(traceback.format_exc())
            hsds_data[hsd_id].summary += "\n\nWARNING: Failed to post summary as a new comment into HSD"
    
    html = build_summary_html(hsds_data)
    
    if delivery in (DELIVERY_EMAIL, DELIVERY_ALL):
        email_connector.sendEmail(toaddr = email_addresses, 
              fromaddr = "ive.genai.hsd_sumarizerl@intel.com", 
              subjectText = "HSD iVE GenAI Summary", 
              bodyText = None,
              htmlText = html,
              )
    
    if delivery in (DELIVERY_HTML, DELIVERY_ALL):
        with open(html_output, "w") as fh:
            fh.write(html)
        print("HTML output written to %s"%(os.path.abspath(html_output),))
        if open_html:
            os.system(html_output)
    
if __name__ == "__main__":
    options = _get_user_inputs()
    
    process_hsds(hsd_ids = options.hsd_ids, 
                 delivery = options.delivery, 
                 post_comment = options.post_comment,
                 email_addresses = options.email_addresses)