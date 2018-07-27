import paho.mqtt.client as mqtt
import time
import json
from bluepy import btle

broker_address = "192.168.0.103"
broker_port = 8246

scan = btle.Scanner()
sec = 1

client1 = mqtt.Client("EFS_App/Fun_Publisher")  # create client object
client1.connect(broker_address, broker_port)  # establish connection


def on_publish(client, userdata, result):
    print("data published \n")
    pass


while True:
    client1.on_publish = on_publish  # assign function to callback
    print("Scanning for %s seconds" % sec)
    devs = scan.scan(sec)
    scan_result = {}
    scan_result['Device_ID'] = "13a52a4263e14895872794d055c9fd0a"
    scan_result['Device_Name'] = "IDCC_Robot"
    lst = []
    for dev in devs:
        local_name = dev.getValueText(9)
        if local_name == 'USBeacon':
            res = {}
            address = dev.addr
            rssi = dev.rssi
            res['Device_Manufacturer'] = local_name
            res['Device_MAC_ADDR'] = address
            res['Device_RSSI'] = rssi
            lst.append(res)

    scan_result['iBeacon_Scan_Results'] = lst
    print(json.dumps(scan_result))

    client1.publish("5G-CORAL_Coarse_Localisation/IDCC_Robot/iBeacon_Scan_Report/", json.dumps(scan_result))
    time.sleep(1)
