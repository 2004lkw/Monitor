# Connection tester routes for the connection testing tool.
# Version 1.0
from flask import Flask, render_template, request, redirect
from flask import jsonify
from os import path
import json
import time
from datetime import datetime, timedelta

#declares
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
        exit()

    if path.exists(historyFilename) is not True:
        # the path for history doesn't exist.
        return render_template('no_info.html')
        exit()

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
        if str(hostname) != "time" and str(hostname) != "Interval":
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




if __name__ == "__main__":
    app.run(host='0.0.0.0')



