#Import JSON and Requests library for program
import json
import requests

#Press "Enter" to begin program
input("Pause.")

#Start receiving data from TTU Swarm Net
print("Getting Data...\n")
r = requests.get('http://172.16.0.1:8001/FieldData/GetData')
print(r.text)
print('\n')
print("Got Data.\n")

#Data from TTU Swarm Net is converted from JSON data to Python dictionary
parsed = json.loads(r.text)

#Dividing up the Python dictionary into smaller dictionaries
#Ball
ball = parsed['Ball']
#Red Team
redTeam = parsed['Red Team Data']
rtCircle = redTeam['Circle']
rtSquare = redTeam['Square']
rtTriangle = redTeam['Triangle']
#Blue Team
blueTeam = parsed ['Blue Team Data']
btCircle = blueTeam['Circle']
btSquare = blueTeam['Square']
btTriangle = blueTeam['Triangle']

#Print out the new smaller dictionaries
print(ball)
print("\n")
print(rtCircle)
print("\n")
print(rtSquare)
print("\n")
print(rtTriangle)
print("\n")
print(btCircle)
print("\n")
print(btSquare)
print("\n")
print(btTriangle)
print("\n")

#Function Complete
input("Function Complete. Press 'Enter' to exit.")
quit()
