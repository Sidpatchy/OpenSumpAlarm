# The main file for OpenSumpAlarm by Sidpatchy
# A project to detect sump pump failure or inadequacy
# More info on GitHub: https://github.com/Sidpatchy/OpenSumpAlarm

# Import libraries
import sLOUT as lout
import os
import time
import board
import datetime as DT
import adafruit_hcsr04

# Import modules
from module.sendEmail import sendEmail
from module.stateChecker import stateChecker

# Sensor Pins
txPin = board.D14
rxPin = board.D15

# Store version info
version = ["v0.1.0-b.1", "2021-03-29"]

# startTime
startTime = lout.time()

# Location of config and log file
config = "config.yml"
logFile = "OpenSumpAlarm.log"

# Parse data from config file

# Sensor values
warnDistance = int(lout.readConfig(config, "warnDistance"))
readTime = float(lout.readConfig(config, "readTime"))

# Email Data
sendGridAPI = str(lout.readConfig(config, "sendGridAPI"))
from_email = str(lout.readConfig(config, "OpenSump_email"))
alertRecipients = lout.readConfig(config, "alertRecipients")
emailSubject = str(lout.readConfig(config, "emailSubject"))
emailContent = str(lout.readConfig(config, "emailContent"))

enabled = True
warn = False
timeLimit = False
emailSendTime = DT.datetime.now()
sonar = adafruit_hcsr04.HCSR04(trigger_pin=txPin, echo_pin=rxPin)

lout.log(config, startTime=startTime, startup=True)

while enabled:
    currentTime = DT.datetime.now()
    sensorValue = stateChecker(sonar, warnDistance, readTime)

    # Because apparently Python thinks "any string" = True
    if sensorValue == True and timeLimit:
        warn = True
        lout.log(config, currentTime, "SENSOR TRIPPED")

    if warn:
        currentTime = DT.datetime.now()
        for email in alertRecipients:
            sendEmail(sendGridAPI, from_email, email, emailSubject, emailContent)
            lout.log(config, currentTime, "Email sent to: {}".format(email))
        emailSendTime = DT.datetime.now() + DT.timedelta(hours=1)
        warn = False

    if currentTime > emailSendTime:
        # if timeLimit, it's okay to log a new event
        # if not timeLimit, an event was logged within the last hour
        timeLimit = True
    else:
        timeLimit = False

    time.sleep(0.5)