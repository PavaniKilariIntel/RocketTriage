import glob
import sys
import timeit
from collections import defaultdict

import hsd_similarity_connector as hsd

# import RocketLogParser as parser
import send_email_connector as email

unique_errors = {}  # set()  # holds lines already seen
exclude_list = ['SWERROR']  # ["fishing", "ignore", "Log Categories", "No error", "Caught PM error while fishing"]
include_list = ['Cpunum', 'FAILURE', r'ERROR:', 'FAIL ', r'(AcreError):']  # ["; PID(", "line #"]
errors = 0
LOG_FILE_NAME = 'SVOS_AI_Output.log'


def scan_log_dir(directory):
    '''
    Scan all logs in directory
    :param directory: rocket log file directory
    :return: unique errors
    '''
    # Get the list of all files and directories
    global total_log_files
    files = glob.glob(directory + '*.log')
    total_log_files = files.__len__()

    # print('Named with wildcard *.log :')
    # Reading each file separately and parsing the results
    for file in files:
        parse_log_file(file)
    results = get_summary()
    return str(unique_errors), results


def parse_log_file(file):
    '''
    Parses each log file and checks for error patterns and add unique error patterns in to set
    :param file: input log file
    :return: None
    '''
    global errors
    with open(file, 'r') as f:
        for line in f:
            line = line.strip()  # .lower()
            # ("error" in line or "fail" in line) and
            if any(substring in line for substring in include_list) and not any(
                    substring in line for substring in exclude_list):
                # for r in regexconf:
                # if re.search(r, line):
                errors = errors + 1
                # Following line generates complete error message,
                # but we are interested in the Rocket application and error msg.
                # uniqErrors.add(f.name.split('\\')[-1] + ", " + line.strip().replace(";", ","))
                # unique_errors.add((f.name.split('\\')[-1]).split("_")[0] + ":" + line.replace(";", ",").split(",")[-1])
                key = (f.name.split('\\')[-1]).split("_")[0]
                # print(line)
                if key not in unique_errors:
                    unique_errors[key] = line#.replace(";", ",").split(",")[-1]
                # unique_errors.add((f.name.split('\\')[-1]) + ":" + line.replace(";", ",").split(",")[-1])
    # print(f"TOTAL ERRORS IN THE LOG {fileName} FILES :: ", errors)


def get_summary():
    '''
    Summary of logs scanned, errors logged and unique error patterns
    :return: dictionary
    '''
    results_dict = defaultdict()
    results_dict["TOTAL LOG FILES SCANNED "] = total_log_files
    results_dict["TOTAL ERRORS LOGGED  "] = errors
    results_dict["TOTAL UNIQUE PATTERNS  "] = unique_errors.__len__()
    return results_dict


def main():
    # logfile = open('SVOS_AI_Output.log', 'w')
    # sys.stdout = sys.stderr = logfile

    # sys.stdout = open('SVOS_AI_Output.log', 'w')
    # sys.stderr = sys.stdout

    start = timeit.default_timer()
    # READING DIR NAME FROM COMMAND LINE
    directory = input(r"Enter the path of Rocket logs folder: ") or (
        "C:\\Pavani\\Projects\\ACE\\GENAI\\Triage\\Rocket\\ROCKET_LOGS\\rocket_extracted_logs\\arden\\")
        # "C:\\Pavani\\Projects\\ACE\\GENAI\\Triage\\Rocket\\ROCKET_LOGS\\Archive\\EXTRACTED\\logs\\")
    print(f"Parsing files in the directory: {directory}")

    errors, summary = scan_log_dir(directory)
    print("ERRORS DETECTED ::")
    # print(errors,summary)
    default_dict = defaultdict()
    # for error in errors:
    errors = errors.replace('\'', '').replace('{', '').replace('}', '')
    print(errors)
    # default_dict[errors] = hsd.get_similar_hsds(errors)
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
    for k, v in summary.items():
        html_body += k + " ::: " + str(v) + " </br>"

    html_body += ''' </br></br></br>
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
            hsds += "<li>" + hsd_n_summary[0] + "</li>"
            ai_summary += "<pre>" + hsd_n_summary[1] + "</pre> </br> <hr> </br>"
        hsds += "</ul>"
        ai_summary += "</ul>"
        html_body += hsds + "</td>" + ai_summary + "</td></tr>"
    html_body += "</table></body>"

    email.sendEmail(toaddr='pswarupa',
                    fromaddr="ive.svosai.rocket@intel.com",
                    subjectText="[Testing PDL] ROCKET Triage Summary - WIP ",
                    # subjectText="ROCKET : HSDs located based on the errors from Rocket failures",
                    bodyText="",
                    htmlText=html_body)


# class Logger(object):
#     def __init__(self):
#         self.terminal = sys.stdout
#         self.log = open("logfile.log", "a")
#
#     def write(self, message):
#         self.terminal.write(message)
#         self.log.write(message)
#
#     def flush(self):
#         # this flush method is needed for python 3 compatibility.
#         # this handles the flush command by doing nothing.
#         # you might want to specify some extra behavior here.
#         pass

class DualOutput:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):  # This flush method is needed for python 3 compatibility.
        # This flushes the stream to the file, but not to the terminal.
        self.log.flush()




if __name__ == "__main__":
    sys.stdout = DualOutput(LOG_FILE_NAME)
    sys.exit(main())
