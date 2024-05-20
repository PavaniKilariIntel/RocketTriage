# import OS module
import glob
import sys
from collections import defaultdict


unique_errors = set()  # holds lines already seen
exclude_list = ["unregister", "fishing", "ignore", "Log Categories", "No error", "Caught PM error while fishing"]
include_list = ["; PID(", "line #"]
errors = 0
total_log_files = 0


def read_log_file(file):
    global errors
    with open(file, 'r') as f:
        for line in f:
            line = line.strip().lower()
            if ("error" in line or "fail" in line) and all(
                    substring.lower() in line for substring in include_list) and not any(
                    substring.lower() in line for substring in exclude_list):
                errors = errors + 1
                # Following line generates complete error message,
                # but we are interested in the Rocket application and error msg.
                # uniqErrors.add(f.name.split('\\')[-1] + ", " + line.strip().replace(";", ","))
                unique_errors.add((f.name.split('\\')[-1]).split("_")[0] + ":" + line.replace(";", ",").split(",")[-1])
    # print(f"TOTAL ERRORS IN THE LOG {fileName} FILES :: ", errors)


def get_results():
    results_dict = defaultdict()
    results_dict["TOTAL LOG FILES SCANNED "] =  total_log_files
    results_dict["TOTAL ERRORS LOGGED  "] =  errors
    results_dict["TOTAL UNIQUE PATTERNS  "] =  unique_errors.__len__()
    return results_dict


def scan_log_dir(directory):
    # Get the list of all files and directories
    global total_log_files
    files = glob.glob(directory + '*.log')
    total_log_files = files.__len__()

    # print('Named with wildcard *.log :')
    for file in files:
        read_log_file(file)
    results = get_results()
    return sorted(unique_errors), results


def main():
    scan_log_dir("C:\\Pavani\\Projects\\ACE\\GENAI\\Triage\\Rocket\\ROCKET_LOGS\\rocket_extracted_logs\\logs2\\")


if __name__ == "__main__":
    sys.exit(main())
