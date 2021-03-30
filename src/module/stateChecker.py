# State checker for OpenSumpAlarm by Sidpatchy
# A project to detect sump pump failure or inadequacy
# More info on GitHub: https://github.com/Sidpatchy/OpenSumpAlarm

# Import libraries
import time
import datetime as DT
import adafruit_hcsr04

# stateChecker(), checks if a sensor has been triggered
# Usage:
#   trigger_pin: board.pin, TX pin
#   echo_pin: board.pin, RX pin
#   warnDistance: float, distance (in centimeters) water should be from sensor to trigger a warning
#   readTime: int or float, time to read from sensor to generate an average (default: 15)
def stateChecker(sonar, warnDistance, readTime=16):
    distances = []
    
    # We take an average distance over a period of time to hopefully prevent false alarms as a result of signal noise/sensor inaccuracies
    endTime = DT.datetime.now() + DT.timedelta(seconds=readTime)
    while endTime > DT.datetime.now():
        #lout.clearScreen()
        try:
            distances.append(sonar.distance)
        except RuntimeError:
            pass
        time.sleep(2)
    
    if sum(distances) == 0:
        return "Sensor returned null value, check your wiring."
    else:
        distAvg = sum(distances) / len(distances)
        distances = []

    print(distAvg)
    if int(distAvg) <= int(warnDistance):
        # If sensor is tripped return True
        return True
    elif int(distAvg) > int(warnDistance):
        # If sensor is tripped return False
        return False
    else:
        return "ERROR: unexpected value passed. Please check your warnDistance."