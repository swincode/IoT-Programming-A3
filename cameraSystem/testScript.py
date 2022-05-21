# Script to quickly send move requests to gimble to test queuing of actions

import paho.mqtt.client as mqtt
from random import randint
from time import sleep

if __name__ == "__main__":
    # Set up MQTT Connection
    client = mqtt.Client("joystick")
    
    # Connect
    client.connect("test.mosquitto.org")

    while True:
        client.publish("joystick/command", f"m {randint(0, 180)} {randint(0, 180)}")
        print("published")
        sleep(0.1)