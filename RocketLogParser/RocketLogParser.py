# import OS module
import glob
import sys

uniqErrors = set()  # holds lines already seen
exclude_list = ["unregister", "fishing", "ignore", "Log Categories", "No error", "Caught PM error while fishing"]
include_list = ["; PID(", "line #"]
errors = 0

def readLogFile(fileName):
    global errors
    with open(fileName, 'r') as f:
        for line in f:
            line = line.strip().lower()
            if ("error" in line or "fail" in line) and all(substring.lower() in line for substring in include_list) and not any(substring.lower() in line for substring in exclude_list):
                errors = errors + 1
                # Following line generates complete error message,
                # but we are interested in the Rocket application and error msg.
                # uniqErrors.add(f.name.split('\\')[-1] + ", " + line.strip().replace(";", ","))
                uniqErrors.add( (f.name.split('\\')[-1]).split("_")[0] + ":" + line.replace(";", ",").split(",")[-1])
    # print(f"TOTAL ERRORS IN THE LOG {fileName} FILES :: ", errors)


def printErrors():
    linenum = 0
    for errorstr in sorted(uniqErrors):
        linenum = linenum + 1
        print(errorstr)
    print("Total Unique Errors found :: ", linenum)


def main():
    # Get the list of all files and directories

    # "C:\\Pavani\\Projects\\ACE\\GENAI\\Triage\\Rocket\\ROCKET_LOGS\\rocket_extracted_logs\\logs2\\"
    # READING DIR NAME FROM COMMAND LINE
    direc = input(r"Enter the path of the folder: ") or (
        "C:\\Pavani\\Projects\\ACE\\GENAI\\Triage\\Rocket\\ROCKET_LOGS\\Archive\\EXTRACTED\\logs\\")
    print(f"Files in the directory: {direc}")
    # if not direc:
    #     direc = "C:/Pavani/Projects/ACE/GENAI/Triage/Rocket/ROCKET_LOGS/Archive/EXTRACTED/logs/"
    #     print("The directory is empty, assign default path :: ", direc)

    x = 0

    # print('Named with wildcard *.log :')
    for files in glob.glob(direc + '*.log'):
        x = x + 1
        readLogFile(files)
    printErrors()
    print("TOTAL ERRORS LOCATED :: ", errors)
    print("TOTAL LOG FILES ::: ", x)


if __name__ == "__main__":
    sys.exit(main())
