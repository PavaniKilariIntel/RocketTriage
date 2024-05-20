import sys
from collections import defaultdict

import RocketLogParser as parser
import hsd_similarity_connector as hsd
import send_email_connector as email


directory = input(r"Enter the path of the folder: ") or (
    "C:\\Pavani\\Projects\\ACE\\GENAI\\Triage\\Rocket\\ROCKET_LOGS\\rocket_extracted_logs\\logs2\\")
    # "C:\\Pavani\\Projects\\ACE\\GENAI\\Triage\\Rocket\\ROCKET_LOGS\\Archive\\EXTRACTED\\logs\\")


def main():
    # READING DIR NAME FROM COMMAND LINE
    print(f"Files in the directory: {directory}")
    # if not directory:
    #     directory = "C:/Pavani/Projects/ACE/GENAI/Triage/Rocket/ROCKET_LOGS/Archive/EXTRACTED/logs/"
    #     print("The directory is empty, assign default path :: ", directory)

    errors, results = parser.scan_log_dir(directory)
    print("ERRORS IN THE ROCKET ::")
    # print(*errors, sep="\n")
    default_dist = defaultdict()
    for error in errors:
        default_dist[error] = hsd.get_similar_hsds(error)

    print("DEFAULT DICTONARY ::: ", default_dist)

    send_email(default_dist, results)


def send_email(default_dist, results):
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
    for k,v in results.items():
        html_body += k + " ::: " + str(v) + " </br>"

    html_body +=''' </br></br></br>
        <table id="ROCKET_ERROR_HSD">
          <tr>
            <th>ROCKET ERROR</th>
            <th>SIMILAR HSD</th>
          </tr>
      '''

    for key, value in default_dist.items():
        html_body += "<tr> <td>" + key + "</td><td><ul>"
        for hsd_urls in value:
            html_body += "<li>" + str(hsd_urls).replace(" ", "") + "</li>"
        html_body += "</ul></td></tr>"
    html_body += "</table></body>"

    email.sendEmail(toaddr='pswarupa',
                    fromaddr="ive.genai.demo.email@intel.com",
                    subjectText="ROCKET : HSDs located based on the errors from Rocket failures",
                    bodyText="",
                    htmlText=html_body)


if __name__ == "__main__":
    sys.exit(main())
