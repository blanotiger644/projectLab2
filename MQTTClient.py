#Informative website: https://pypi.org/project/paho-mqtt/#subscribe-unsubscribe
#Server Setup: https://tutorials-raspberrypi.com/raspberry-pi-mqtt-broker-client-wireless-communication/

#This code will have code to send and receive MQTT messages
import paho.mqtt.client as mqtt #paho-mqtt library
import time

#define certain functions:
#on_connect to the MQTT server:
def on_connect(client,userdata,flags,rc):
    print("Connection resulted in: "+connack_string(rc))
    client.subscribe("blanotiger/ledStatus") #subscribes upon connect
#on_disconnect to the MQTT server:    
def on_disconnect(client,userdata,rc):
    if rc!= 0:
        print("Unexpected disconnection.")
        client.reconnect()
#on_message from the MQTT server:        
def on_message(client,userdata,message):
    print("Received message '"+str(message.payload)+"' on topic '"+message.topic+"' with QoS "+str(message.qos))
    msg = str(message.payload)
    
#This code will connect to the broker:
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
client.connect("blanotiger", 1883, 60) #Formatted (address, port, keepalive(seconds))

#This code will subscribe to a topic:
#print("Subscribing to topic 'blanotiger/ledStatus'...")
#client.subscribe("blanotiger/ledStatus",0)
#print("Subscribed!")

#This code will send a message:
print("Sending 0...")
client.publish("blanotiger/ledStatus",payload="0") #This is formatted (topic,message,qos,retain)
time.sleep(1) #Wait for 1 second
print("Sending 1...")
client.publish("blanotiger/ledStatus",payload="1") #This is formatted (topic,message,qos,retain)

#WILL_SET() sets a message to be published by the broker if the client disconnects without a disconnect() function
WILL_SET("blanotiger/ledStatus","Client 1 disconnected",)

#This code will reconnect if the client ever accidentally disconnects:
client.reconnect()

#This code will disconnect if called:
client.wait_for_publish()
client.disconnect()
