import sys
from collections import defaultdict
import timeit

import RocketLogParser as parser
import hsd_similarity_connector as hsd
import send_email_connector as email

directory = input(r"Enter the path of the folder: ") or (
    "C:\\Pavani\\Projects\\ACE\\GENAI\\Triage\\Rocket\\ROCKET_LOGS\\rocket_extracted_logs\\arden\\")
    # "C:\\Pavani\\Projects\\ACE\\GENAI\\Triage\\Rocket\\ROCKET_LOGS\\Archive\\EXTRACTED\\logs\\")


def main():
    start = timeit.default_timer()
    # READING DIR NAME FROM COMMAND LINE
    print(f"Parsing files in the directory: {directory}")

    errors, summary = parser.scan_log_dir(directory)
    print("ERRORS IN THE ROCKET ::")
    print(*errors, sep="\n")
    default_dict = defaultdict()
    # for error in errors:
    #     default_dict[error] = hsd.get_similar_hsds(error)
    #
    # # print("DEFAULT DICTONARY ::: ", default_dict)
    #
    # send_email(default_dict, summary)

    stop = timeit.default_timer()

    print('\n\nTotal Execution Time: ', stop - start)


def send_email(default_dict, summary):
    html_body = '''
    <header>
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
            #ROCKET_ERROR_HSD {
              font-family: Arial, Helvetica, sans-serif;
              border-collapse: collapse;
              width: 100%;
            }
            
            #ROCKET_ERROR_HSD td, #ROCKET_ERROR_HSD th {
              border: 1px solid #ddd;
              padding: 8px;
            }
            
            #ROCKET_ERROR_HSD tr:nth-child(even){background-color: #f2f2f2;}
            
            #ROCKET_ERROR_HSD tr:hover {background-color: #ddd;}
            
            #ROCKET_ERROR_HSD th {
              padding-top: 12px;
              padding-bottom: 12px;
              text-align: left;
              background-color: #04AA6D;
              color: white;
            }
        </style>
        <body>
    </br>
    Hi Team,
    </br></br>
    Please find the Rocket Triage results below.
    </br></br></br>
    '''
    for k,v in summary.items():
        html_body += k + " ::: " + str(v) + " </br>"

    html_body +=''' </br></br></br>
        <table id="ROCKET_ERROR_HSD">
          <tr>
            <th>ROCKET ERROR</th>
            <th>SIMILAR HSDs</th>
            <th>OpenAI Summary</th>
          </tr>
      '''

    for key, value in default_dict.items():
        html_body += "<tr> <td>" + key + "</td>"
        hsds = "<td><ul>"
        ai_summary = "<td style=font size =-2><ul>"
        for hsd_urls in value:
            hsd_n_summary = str(hsd_urls).replace(" ", "").split(":::")
            hsds+="<li>"+hsd_n_summary[0]+"</li>"
            ai_summary+="<pre>"+hsd_n_summary[1]+"</pre> </br> <hr> </br>"
        hsds+="</ul>"
        ai_summary+="</ul>"
        html_body += hsds+"</td>"+ai_summary+"</td></tr>"
    html_body += "</table></body>"

    email.sendEmail(toaddr='pswarupa',
                    fromaddr="ive.svosai.rocket@intel.com",
                    subjectText="[Testing PDL] ROCKET Triage Summary - WIP ",
                    # subjectText="ROCKET : HSDs located based on the errors from Rocket failures",
                    bodyText="",
                    htmlText=html_body)


if __name__ == "__main__":
    sys.exit(main())
