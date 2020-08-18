# Connection tester routes for the connection testing tool.
# Version 1.0
from flask import Flask, render_template, request, redirect, make_response
from flask import jsonify
from os import path
import os
import json
import time
from datetime import datetime, timedelta

#declares
hostsFilename = "hosts.txt"
resultsFilename = "hostspings.txt"
historyFilename = "hostshistory.txt"
# Literal strings used to build the HTML
host_heading = """<tr><td><h3>"""
host_closing = """</h3></td><td></td></tr>"""

host_progress = """<tr><td><div class='bar-container' id='""" #need the id here
host_progress2 = """'>""" # add all boxgreen/yellow/red
host_progress_end = "</div></td><td>"

box_green="""<div class="box-green" data-toggle="tooltip" title='""" # insert time
box_green_end = """'></div>"""

box_red="""<div class="box-red" data-toggle="tooltip" title='""" # insert time
box_red_end = """'></div>"""

led_green = """<div class="led-green led-spacer"></div>"""
led_red = """<div class="led-red led-spacer"></div>"""
led_yellow = """<div class="led-yellow led-spacer"></div>"""



app = Flask(__name__)

# MAIN ROUTE ******************************************************************
@app.route("/")
def main_route():
    # default Route.
    if path.exists(resultsFilename) is not True:
        # the path for results doesn't exist.
        return render_template('no_info.html')

    if path.exists(historyFilename) is not True:
        # the path for history doesn't exist.
        return render_template('no_info.html')

    # open the results and history files and read them. (as json)
    with open(resultsFilename, "r") as fileHandle:
        hostResults = json.load(fileHandle)
    with open(historyFilename,"r") as fileHandle:
        historyResults = json.load(fileHandle)

    template_output = "" # string used to format the output for Jinja2 (through flask)
    startTime = datetime.strptime(hostResults["time"], "%H:%M:%S") # time of most recent check.
    timeInterval = hostResults["Interval"] # interval of checks done.

    for hostname in hostResults:
        # filter out for "time", "Interval" to stop errors.
        if str(hostname) != "time" and str(hostname) != "Interval" and str(hostname) != "":
            #Build the dynamic HTML based off the data. 
            template_output = template_output + host_heading + hostname + host_closing # this is row 1, col 1 and 2 of the table
            historyStr = historyResults[hostname] # get the history for this hostname.
            template_output = template_output + host_progress + hostname + host_progress2
            # Add the history, starting with the time.
            thisHostTimeStart = startTime - timedelta(hours = 0, minutes = timeInterval * len(historyResults[hostname]))
            thisHostTimeStart2 = time.strptime(str(thisHostTimeStart),"%Y-%m-%d %H:%M:%S" )
            thisHostTimeStartStr = time.strftime("%H:%M:%S", thisHostTimeStart2)
            markerCount = 0
            for marker in historyResults[hostname]:
                thisMarkerTime = thisHostTimeStart + timedelta(hours=0, minutes = timeInterval * markerCount)
                thisMarkerTime = time.strptime(str(thisMarkerTime),"%Y-%m-%d %H:%M:%S" )
                thisMarkerTimeStr = time.strftime("%H:%M:%S" , thisMarkerTime)
                if marker == "!":
                    template_output = template_output + box_green + thisMarkerTimeStr + box_green_end # replace "2" with a relative time
                else:
                    template_output = template_output + box_red + thisMarkerTimeStr + box_red_end # replace "2" with a relative time
                markerCount += 1
            template_output = template_output + host_progress_end
            # add the status indicator.
            if "!" in historyResults[hostname] and "." in historyResults[hostname]:
                # use a yellow LED
                template_output = template_output + led_yellow
            elif "!" in historyResults[hostname]:
                # Gets the green
                template_output = template_output + led_green
            else:
                #RED!
                template_output = template_output + led_red
            template_output = template_output +"</td></tr>"

            # current time.
            timeCur = datetime.now()
            cur_time_date = timeCur.strftime("%m/%d/%Y %H:%M")

    #End of route.
    return render_template('index.html',template_output=template_output,cur_time_date= cur_time_date)


@app.route("/gethosts", methods=['GET'])
def gethosts_route():
    # get the hosts and send as a JSON to the front end.
    if path.exists(historyFilename) is not True:
        # the path for the hosts file doesn't exist.
        render_template('no_info.html'), 404
        exit()
    # open the file as a JSON
    hosts={}
    with open(hostsFilename, "r") as fileHandle:
        for host in fileHandle:
            # load each host as a str, remove new lines, and create a dictionary 
            newhost = str(host)
            newhost = newhost.rstrip("\n")
            hosts[newhost]=newhost
    #return the JSON!
    return hosts # don't need to jsonify() this since it'a  dict.

@app.route("/addhost", methods=['POST'])
def sethost_route():
    # add a new host if the value is good.
    hostAdd = request.get_json()
    # this should be a host = 
    try:
        # try getting host.
        addThisHost = hostAdd['host']
    except:
        # didn't work.  Request doesn't work.  exit.
        exit()
    if "'" in addThisHost or '"' in addThisHost or "&" in addThisHost or " " in addThisHost or "!" in addThisHost:
        # INVALID CHARACTERS.  DO NOT ALLOW THESE TO BE SAVED
        exit()
    else:
        # Add this host to the list.
        with open(hostsFilename, "a") as fileHandle:
            fileHandle.write("\n"+addThisHost)
    # we got here so it's been added.  Let the browser know:
    outStat = jsonify(success=True)
    outStat.status_code = 200
    return outStat

@app.route("/deletehost", methods=['POST'])
def removehost_route():
    # get the host requested to remove.
    hostReq = request.get_json()
    hostToRemove = hostReq['remove']
    print("'"+hostToRemove+"'")
    # this is just a host = host JSON with one line.
    with open(hostsFilename,"r") as hostsRead:
        with open("tmpHosts.txt", "w") as hostsWrite:
            for txtIn in hostsRead:
                txtIn=txtIn.rstrip("\n")
                if txtIn != hostToRemove and txtIn != "":
                    hostsWrite.write(txtIn+"\n")
    # delete the old one, rename the new one.
    os.remove(hostsFilename)
    os.rename("tmpHosts.txt", hostsFilename)
    # Exit the route with a return to the browser.    
    outStat = jsonify(success=True)
    outStat.status_code = 200
    return outStat

@app.route("/refresh", methods=['POST'])
def refresh_route():
    req = request.get_json()
    if req['refresh'] == 'now':
        # requested to refresh.
        os.system('python3 connection_tester.py')
    outStat = jsonify(success=True)
    outStat.status_code = 200
    return outStat

if __name__ == "__main__":
    app.run(host='0.0.0.0')



