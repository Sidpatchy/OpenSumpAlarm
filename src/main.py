# The main file for OpenSumpAlarm by Sidpatchy
# A project to detect sump pump failure or inadequacy
# More info on GitHub: https://github.com/Sidpatchy/OpenSumpAlarm

# Import libraries
import module.sLOUT as lout
import os
from time import sleep
from datetime import timedelta

# Import modules
from module.sendEmail import sendEmail
from module.stateChecker import stateChecker

# Sensor Pin
#sensorPin = board.D10

# Store version info
version = ["v0.1.0-a.2", "2021-03-26"]

# Location of config and log file
config = "config.yml"
logFile = "OpenSumpAlarm.log"

# Parse data from config file

# Email Data
sendGridAPI = str(lout.readConfig(config, "sendGridAPI"))
from_email = str(lout.readConfig(config, "OpenSump_email"))
alertRecipients = lout.readConfig(config, "alertRecipients")
emailSubject = str(lout.readConfig(config, "emailSubject"))
emailContent = str(lout.readConfig(config, "emailContent"))

enabled = True
warn = False
emailSendTime = lout.time()
sensorPin = 4

while enabled:
    time = lout.time()
    sensorValue = stateChecker(sensorPin)

    if warn:
        time = lout.time()
        for email in alertRecipients:
            sendEmail(sendGridAPI, from_email, email, emailSubject, emailContent)
            lout.log(logFile, time, "Email sent to: {}".format(email))
        emailSendTime = lout.time() + timedelta(hours=1)
        warn = False

    if time > emailSendTime:
        # if timeLimit, it's okay to log a new event
        # if not timeLimit, an event was logged within the last hour
        timeLimit = True
    else:
        timeLimit = False

    if sensorValue and timeLimit:
        warn = True
        lout.log(logFile, time, "SENSOR (pin {}) TRIPPED".format(sensorPin))

    sleep(0.5)