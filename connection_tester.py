import sys
import platform    # For getting the operating system name
import subprocess  # For executing a shell command
import os.path   # for file stuff.
import json # used for file output.
from os import path
import time
# This will ping all hosts in a file and attempt to write out to file if there was a success.
# Version 1.0  (Test and complete on 8/8/2020)

# variable set up.
t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)
hosts = [] # these will be read from file.
hostsWithResults = {} # dictionary to save results and hosts in matching pairs 
hostsFile = "hosts.txt" # name of the hosts file.
outputFilename = "hostspings.txt" # output of the file.
historyFilename = "hostshistory.txt" # where to store the output of the history of the hosts.
interval_amount = 2 # minutes in between checks.
max_history = 40 # max history to keep.
DONT_RUN_FILENAME = "connection_no_run.tmp" # this file is to make sure that this script isn't already running.

# function to ping with.
def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """
    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower() == 'windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]

    return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0


if path.exists(DONT_RUN_FILENAME):
    # don't run file exists.  Stop script here.
    exit()

# Load the hosts file here.
if path.exists(hostsFile) is not True:
    # Files doesn't exist.  Exit.
    exit()
else:
    fileHandle = open(hostsFile,"r")
    # TODO: Change this to a with statement.
    # for each line in this file, remove the \n and save it as a string to the dictionary.
    for linecounter in fileHandle:
        newLine = str(linecounter)
        newLine = newLine.rstrip("\n")
        hosts.append(newLine)
    fileHandle.close()
    # create a tmp file telling this script not to run. ***** This is where the tmp file is made *****
    with open(DONT_RUN_FILENAME, "w") as dontRunFile:
        dontRunFile.write("DONT_RUN")

# Main code here.
for counts in hosts:
    results = ping(counts)
    hostsWithResults[counts] = results # store this result with this host in the dictionary.

# save the history.
# 1 if there is a history, load it first.
hostsHistory={}
if path.exists(historyFilename) is not True:
    # no history exists.  Create the dict
    for n in hostsWithResults:
        n=n.rstrip("\n")
        if hostsWithResults[n] == True:
            hostsHistory[n] = "!"
        else:
            hostsHistory[n] = "."
    # convert the results in to a JSON
    output_history = json.dumps(hostsHistory, indent = 4)
    # output the JSON to a file.
    with open(historyFilename,"w") as outputFilehandle:
        json.dump(hostsHistory,outputFilehandle)
else:
    # The file exists.  load, compare, update and write.
    with open(historyFilename,"r") as fileHandle:
        historyFromFile = json.load(fileHandle)
    for n in hostsWithResults:
        n=n.rstrip("\n")
        # if the host we tested is existing in the file contents, copy and update.  Else, add.
        if n in historyFromFile:
            if hostsWithResults[n]==True:
                outChar = "!"
            else:
                outChar="."
            # since we have the history, add the ! or .
            outputString = historyFromFile[n]+outChar
            if len(outputString) > max_history:
                #new history is too long. Need last 
                outputString = outputString[-max_history:]
            hostsHistory[n]=outputString
        else:
            # This host doesn't exist in history.
            if hostsWithResults[n]==True:
                outChar = "!"
            else:
                outChar="."
            hostsHistory[n]=outChar
        # convert the results in to a JSON
    output_history = json.dumps(hostsHistory, indent = 4)
    # output the JSON to a file.
    with open(historyFilename,"w") as outputFilehandle:
        json.dump(hostsHistory,outputFilehandle)
    # Done trying to determine what's what.  Now lets write the thing out to file.

#add time
hostsWithResults["time"]=current_time

#add interval (for calculation later in the monitor.py module)
hostsWithResults["Interval"]=interval_amount

# Convert Dictionary to JSON
jsonRep = json.dumps(hostsWithResults,  indent = 4)

# Write results to file.
with open(outputFilename,"w") as outputFilehandle:
    json.dump(hostsWithResults,outputFilehandle)

# finally, delete our file we made to keep this from running in parallel.
os.remove(DONT_RUN_FILENAME)
