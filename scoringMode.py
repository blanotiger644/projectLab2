#Libraries
import paho.mqtt.client as mqtt
import json
import requests
import time

msg = ""
newparsed = ""
getPath = "http://192.168.137.1:8001/FieldData/GetData"

def phase1():
    print("phase1()")
    newparsed = ""
    oldparsed = newparsed
    r = requests.get(getPath)
    parsed = json.loads(r.text)
    newparsed = parsed["Blue Team Data"]["Circle"]["Object Center"]['X']
    time.sleep(1)
    oldparsed = newparsed
    r = requests.get(getPath)
    parsed = json.loads(r.text)
    newparsed = parsed["Blue Team Data"]["Circle"]["Object Center"]['X']
    while oldparsed==newparsed:
        print(str(newparsed))
        print("Data did not update.")
        time.sleep(1)
        r = requests.get(getPath)
        parsed = json.loads(r.text)
        newparsed = parsed["Blue Team Data"]["Circle"]["Object Center"]['X']
    info1 = parsed["Blue Team Data"]["Circle"]["Object Center"]['X']
    info2 = parsed["Blue Team Data"]["Circle"]["Object Center"]['Y']
    info3 = parsed["Ball"]["Object Center"]['X']
    info4 = parsed["Ball"]["Object Center"]['Y']
    client.publish("blanotiger/robot1",payload=("["+str(info1)+"]["+str(info2)+"]["+str(info3)+"]["+str(info4)+"]"),qos=0,retain=False) #This is formatted (topic,message)

def phase2():
    print("phase2()")
    newparsed = ""
    oldparsed = newparsed
    r = requests.get(getPath)
    parsed = json.loads(r.text)
    newparsed = parsed["Blue Team Data"]["Triangle"]["Object Center"]['X']
    time.sleep(1)
    oldparsed = newparsed
    r = requests.get(getPath)
    parsed = json.loads(r.text)
    newparsed = parsed["Blue Team Data"]["Triangle"]["Object Center"]['X']
    while oldparsed==newparsed:
        print("Data did not update.")
        r = requests.get(getPath)
        parsed = json.loads(r.text)
        newparsed = parsed["Blue Team Data"]["Triangle"]["Object Center"]['X']
    info1 = parsed["Blue Team Data"]["Triangle"]["Object Center"]['X']
    info2 = parsed["Blue Team Data"]["Triangle"]["Object Center"]['Y']
    info3 = parsed["Ball"]["Object Center"]['X']
    info4 = parsed["Ball"]["Object Center"]['Y']
    client.publish("blanotiger/robot3",payload=("["+str(info1)+"]["+str(info2)+"]["+str(info3)+"]["+str(info4)+"]"),qos=0,retain=False) #This is formatted (topic,message)

def everythingStop():
    client.publish("blanotiger/robot3",payload="stop",qos=0,retain=False)
    client.publish("blanotiger/robot1",payload="stop",qos=0,retain=False)
    client.publish("blanotiger/fin",payload="IT'S TIME TO STOP",qos=0,retain=False)

#on_connect to the MQTT server:
def on_connect(client,userdata,flags,rc):
    print("Connection resulted in: "+connack_string(rc))
    client.subscribe("blanotiger/fin") #subscribes upon connect
#on_disconnect to the MQTT server:    
def on_disconnect(client,userdata,rc):
    if rc!= 0:
        print("Unexpected disconnection.")
        client.reconnect()
#on_message from the MQTT server:        
def on_message(client,userdata,message):
    message.payload = message.payload.decode("utf-8")
    print("Received message '"+str(message.payload)+"' on topic '"+message.topic+"'.")
    msg = str(message.payload)
    if msg=="start":
        msg=""
        phase1()
        print("Phase 1 activated.")
    elif msg=="Bot 1 Complete":
        msg=""
        phase2()
        print("Phase 2 activated.")
    elif msg=="Bot 3 Complete":
        msg=""
        everythingStop()
    elif msg=="IT'S TIME TO STOP":
        while True:
            print("IT'S TIME TO STOP")
            time.sleep(5)

#This code will connect to the broker:
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
client.connect("192.168.137.124", 1883, 60) #Formatted (address, port, keepalive(seconds))

print("Subscribing to topic 'blanotiger/fin'...")
client.subscribe("blanotiger/fin",0)
print("Subscribed!")

input("Press Enter to begin Scoring Mode.")

client.publish("blanotiger/fin",payload="start",qos=0,retain=False) #optointeruppter 852-GP1S51VJ000F

client.loop_forever()
