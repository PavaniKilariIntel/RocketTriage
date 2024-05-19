import sys

# SAMPLE INPUT FROM THE TEXT FILE BELOW
# qcontroller2_pid99633.log, Tue May 14 15:09:10, PID(99633), q_controller.cpp, initialize(), line #716, ERROR : Unable to connect to TMAN
# cegrand_pid330436.log, Thu Feb 01 06:01:12, PID(330436), tarmanIPC.c, tmanInitWithSemaphore(), line #626, **ERROR: TMAN - failed to initalize the semaphore for the targets

maxstrings = set()
def main():
    with open('errorlog.txt', 'r') as f:
        linecount = 0
        for line in f:
            if(line.strip().split(",").__len__() > 2):
                errmsg = (line.strip().split(",")[0]).split("_")[0] + ":" + line.strip().split(",")[-1]
                maxstrings.add(errmsg)
                linecount = linecount +1
                print(errmsg)
            # print(line.strip().split("_pid")[0])
    print("TOTAL LINES :: ", linecount)
    print("UNIQRE :: ", maxstrings.__len__())


if __name__ == "__main__":
    sys.exit(main())
