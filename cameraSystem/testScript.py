# Script to quickly send move requests to gimble to test queuing of actions

from tb_device_mqtt import TBDeviceMqttClient
from random import randint
from time import sleep

if __name__ == "__main__":
    # Set up MQTT Connection
    client = TBDeviceMqttClient("demo.thingsboard.io", "qSPi2bDBvBJaPJwcFrTX")

    # Connect to ThingsBoard
    client.connect()

    while True:
        client.send_attributes({"command" : f"m {randint(0, 180)} {randint(0, 180)}"})
        sleep(0.1)