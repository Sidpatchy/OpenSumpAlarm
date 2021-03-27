# State checker for OpenSumpAlarm by Sidpatchy
# A project to detect sump pump failure or inadequacy
# More info on GitHub: https://github.com/Sidpatchy/OpenSumpAlarm

# Import libraries
import datetime as DT
import RPi.GPIO as GPIO

# stateChecker(), checks if a sensor has been triggered
# Usage:
#   sensorPin: board.pin, pin to 
def stateChecker(sensorPin):
    #GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BCM) # Use physical pin numbering
    GPIO.setup(sensorPin, GPIO.IN)

    endTime = DT.datetime.now() + DT.timedelta(seconds=5)
    detected = False
    while endTime > DT.datetime.now():
        sensorStatus = GPIO.input(sensorPin)
        if sensorStatus == 1:
            detected = True
            print("FUCK")
    GPIO.cleanup()

    if detected:
        # If sensor is tripped return True
        return True
    elif not detected:
        # If sensor is tripped return False
        return False
    else:
        return "ERROR: sensor returned an unexpected value."