# import OS module
import glob
import sys
from collections import defaultdict

unique_errors = set()  # holds lines already seen
exclude_list = ['SWERROR']  # ["fishing", "ignore", "Log Categories", "No error", "Caught PM error while fishing"]
include_list = ['Cpunum', 'FAILURE', r'ERROR:', 'FAIL ', ]  # ["; PID(", "line #"]

errors = 0
total_log_files = 0


def parse_log_file(file):
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
                unique_errors.add((f.name.split('\\')[-1]) + ":" + line.replace(";", ",").split(",")[-1])
    # print(f"TOTAL ERRORS IN THE LOG {fileName} FILES :: ", errors)


def get_summary():
    results_dict = defaultdict()
    results_dict["TOTAL LOG FILES SCANNED "] = total_log_files
    results_dict["TOTAL ERRORS LOGGED  "] = errors
    results_dict["TOTAL UNIQUE PATTERNS  "] = unique_errors.__len__()
    return results_dict


def scan_log_dir(directory):
    # Get the list of all files and directories
    global total_log_files
    files = glob.glob(directory + '*.log')
    total_log_files = files.__len__()

    # print('Named with wildcard *.log :')
    # Reading each file separately and parsing the results
    for file in files:
        parse_log_file(file)
    results = get_summary()
    return sorted(unique_errors), results


def main():
    errors, summary = scan_log_dir("C:\Pavani\Projects\ACE\GENAI\Triage\Rocket\ROCKET_LOGS\Archive\EXTRACTED\logs\\")
    # ("C:\\Pavani\\Projects\\ACE\\GENAI\\Triage\\Rocket\\ROCKET_LOGS\\rocket_extracted_logs\\arden\\")
    print("ERRORS IN THE ROCKET ::")
    print(*errors, sep="\n")


if __name__ == "__main__":
    sys.exit(main())
