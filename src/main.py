# The main file for OpenSumpAlarm by Sidpatchy
# A project to detect sump pump failure or inadequacy
# More info on GitHub: https://github.com/Sidpatchy/OpenSumpAlarm

# Import libraries
import module.sLOUT as lout
import os
from time import sleep

# Import modules
from module.sendEmail import sendEmail

# Store version info
version = ["v0.1.0-a.1", "2021-03-24"]

# Location of config file
config = "config.yml"

# Parse data from config file

# Email Data
sendGridAPI = str(lout.readConfig(config, "sendGridAPI"))
from_email = str(lout.readConfig(config, "OpenSump_email"))
alertRecipients = lout.readConfig(config, "alertRecipients")
emailSubject = str(lout.readConfig(config, "emailSubject"))
emailContent = str(lout.readConfig(config, "emailContent"))

enabled = True
warn = False

while enabled:
    if warn:
        time = lout.time()
        for email in alertRecipients:
            sendEmail(sendGridAPI, from_email, email, emailSubject, emailContent)
