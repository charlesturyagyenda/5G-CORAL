import paho.mqtt.client as mqttClient
import time
import json
from operator import itemgetter


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected  # Use global variable
        Connected = True  # Signal connection
    else:
        print("Connection failed")


def on_message(client, userdata, message):
    iBeacon_locations = [{"iBeacon_Addr": "50:33:8b:2d:b9:21", "iBeacon_Region": "Region_1",
                          "iBeacon_LiDAR_Coordinates": {"X_Cod": 1, "Y_Cod": 1, "Z_Cod": 1}},
                         {"iBeacon_Addr": "50:33:8b:2d:98:ce", "iBeacon_Region": "Region_2",
                          "iBeacon_LiDAR_Coordinates": {"X_Cod": 1, "Y_Cod": 2, "Z_Cod": 1}},
                         {"iBeacon_Addr": "50:33:8b:2d:b2:da", "iBeacon_Region": "Region_3",
                          "iBeacon_LiDAR_Coordinates": {"X_Cod": 2, "Y_Cod": 1, "Z_Cod": 1}},
                         {"iBeacon_Addr": "50:33:8b:2d:b2:d3", "iBeacon_Region": "Region_4",
                          "iBeacon_LiDAR_Coordinates": {"X_Cod": 2, "Y_Cod": 2, "Z_Cod": 1}}]

    msg = json.loads(message.payload)
    x = msg['iBeacon_Scan_Results']
    sorted_x = sorted(x, key=itemgetter("Device_RSSI"), reverse=True)

    for k in range(len(iBeacon_locations)):
        if iBeacon_locations[k]['iBeacon_Addr'] == sorted_x[0]['Device_MAC_ADDR']:
            estimated_location = iBeacon_locations[k]['iBeacon_Region']

    client.publish("5G-CORAL_Coarse_Localisation/IDCC_Robot/Estimated_Location/", estimated_location)
    print(estimated_location)
    print "##################"


Connected = False  # global variable for the state of the connection
broker_address = "10.6.224.107"
broker_port = 8246

client2 = mqttClient.Client("Coarse_Localisation_Computation")  # create new instance

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
