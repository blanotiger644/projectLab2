#initalization
import time
import math
import json
import requests
import rotateFunction as rotate
import pwm0 as pwm

getPath = "http://192.168.137.1:8001/FieldData/GetData"
robotValue = ""
teamValue = 0
teamName = ""
areaX = 0
areaY1 = 0
areaY2 = 0
finalX = 0
finalY = 0

#Get Function
def getData:
    global parsed
    global getPath
    r = requests.get(getPath, timeout=2)
    parsed = json.loads(r.text)

#Set Teams
if teamValue == 1:
    areaX = 60
    finalX = 25
    teamName = "Red Team Data"
    if robotValue == "robot1"
        areaY1 = 31
        areaY2 = 105
        finalY = 80
    elif robotValue == "robot2"
        areaY1 = 105
        areaY2 = 145
        finalY = 115
    elif robotValue == "robot3"
        areaY1 = 145
        areaY2 = 220
        finalY = 150
elif teamValue == 2:
    areaX = 335
    finalX = 375
    teamName = "Blue Team Data"
    if robotValue == "robot1"
        areaY1 = 145
        areaY2 = 220
        finalY = 150
    elif robotValue == "robot2"
        areaY1 = 105
        areaY2 = 145
        finalY = 115
    elif robotValue == "robot3"
        areaY1 = 31
        areaY2 = 105
        finalY = 80
    
#Inital Get Request
r = requests.get(getPath, timeout=2)
parsed = json.loads(r.text)

#Setup phase
if robotValue == "robot1":
    rotate.rotate(-90)
    while parsed[teamName]["Circle"]["Object Center"]["Y"] > finalY:
        pwm.forward(10)
        time.sleep(0.5)
        getData()
    rotate.rotate(-90)
    while parsed[teamName]["Circle"]["Object Center"]["X"] > finalX:
        pwm.forward(10)
        time.sleep(0.5)
        getData()
    rotate.rotate(180)
elif robotValue == "robot2":
    rotate.rotate(180)
    while parsed[teamName]["Square"]["Object Center"]["X"] > finalX:
        pwm.forward(10)
        time.sleep(0.5)
        getData()
    rotate.rotate(180)
elif robotValue == "robot3":
    rotate.rotate(90)
    while parsed[teamName]["Triangle"]["Object Center"]["Y"] > finalY:
        pwm.forward(10)
        time.sleep(0.5)
        getData()
    rotate.rotate(90)
    while parsed[teamName]["Triangle"]["Object Center"]["X"] > finalX:
        pwm.forward(10)
        time.sleep(0.5)
        getData()
    rotate.rotate(180)

#Defend Phase
while True:
    getData()
    ballX = parsed["Ball"]["Object Center"]["X"]
    ballY = parsed["Ball"]["Object Center"]["Y"]
    if robotValue == "robot1":
        while ballY >= areaY:
            if teamValue == 1:
                if ballX <= areaX:
                    print("Ball is within Robot 1 area.")
            if teamValue == 2:
                if ballX >= areaX:
                    print("Ball is within Robot 1area.")
    elif robotValue == "robot2":
        while (ballY <= areaY + 20) or (ballY >= areaY - 20):
            if teamValue == 1:
                if ballX <= areaX:
                    print("Ball is within Robot 2 area.")
            if teamValue == 2:
                if ballX >= areaX:
                    print("Ball is within Robot 2 area.")
    elif robotValue == "robot3":
        while ballY <= areaY:
            if teamValue == 1:
                if ballX <= areaX:
                    print("Ball is within Robot 3 area.")
            if teamValue == 2:
                if ballX >= areaX:
                    print("Ball is within Robot 3 area.")
