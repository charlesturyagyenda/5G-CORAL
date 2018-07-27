import paho.mqtt.client as mqttClient
import time


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected  # Use global variable
        Connected = True  # Signal connection
    else:
        print("Connection failed")


def on_message(client, userdata, message):
    print "Message received: " + message.payload
    print client._client_id
    print "##################"


Connected = False  # global variable for the state of the connection
broker_address = "10.6.224.107"
broker_port = 8246

client2 = mqttClient.Client("EFS_App/Fun_Subscriber")  # create new instance

client2.on_connect = on_connect  # attach function to callback
client2.on_message = on_message  # attach function to callback

client2.connect(broker_address, port=broker_port)  # connect to broker

client2.loop_start()  # start the loop

time.sleep(1)  # Wait for 1 second for connection with broker

client2.subscribe("5G-CORAL_Coarse_Localisation/IDCC_Robot/iBeacon_Scan_Report/")

try:
    while True:
        time.sleep(0.0001)

except KeyboardInterrupt:
    print "exiting"
    client2.disconnect()
    client2.loop_stop()
