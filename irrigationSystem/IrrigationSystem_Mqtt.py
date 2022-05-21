import os
import time
import sys
import paho.mqtt.client as mqtt
from tb_device_mqtt import TBDeviceMqttClient
import json
import serial
import random
from time import sleep
  

class DataController:
    def __init__(self, name:str):
        self.moClient = mqtt.Client(name)
        self.moClient.connect("test.mosquitto.org")
        self.moClient.subscribe("joystick/power")
        self.moClient.on_message = self.get_msg
        self.power_state = False
    
    def __del__(self):
        self.moClient.loop_stop()
        self.moClient.disconnect()

    def get_msg(self, client, userdata, message: str) -> None:
        data = message.payload.decode("utf-8")
        self.power_state = data

    def get_data(self) -> None:
        return {"state":self.power_state}

device='/dev/ttyS0'

arduino= serial.Serial(device,9600)


    
THINGSBOARD_HOST = 'demo.thingsboard.io'
ACCESS_TOKEN = 'Irrigation_System_Token'


# Data capture and upload interval in seconds. Less interval will eventually hang the DHT22.
INTERVAL=2

sensor_data = {'temperature': 0, 'humidity': 0}

next_reading = time.time() 

client = mqtt.Client()

# Set access token
client.username_pw_set(ACCESS_TOKEN)

# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(THINGSBOARD_HOST, 1883, 60)

client.loop_start()

 
try:
    while True:
        data= arduino.readline()
        data1= arduino.readline()
        data2= arduino.readline()
        data3= arduino.readline()
        data = float (data)
        data1= float (data1)
        data2= float (data2)
        data3 = float (data3)
        
        lighValue= data
        moistValue=data1
        humidity= data2
        temperature = data3
        humidity = round(humidity, 2)
        temperature = round(temperature, 2)
        data_controller = DataController("irrigation")
        data_controller.moClient.loop_start()

        changePin = data_controller.get_data()

        if changePin == {'state': True}:
            arduino.write(b"3")
            message = "Pump Turned" + "on."
            print(changePin)
        if changePin == {'state': False}:
            arduino.write(b"4")
            message = "Pump Turned" +"off."
            
        print(changePin)   

     
        print(u"Ligh Value: {:g}, Moist Value {:g}, Temperature: {:g}\u00b0C, Humidity: {:g}%".format(lighValue, moistValue, temperature, humidity))
        sensor_data['Temperature'] = temperature
        sensor_data['Humidity'] = humidity
        sensor_data['Ligh Value'] = lighValue
        sensor_data['Moist Value'] = moistValue
        

        # Sending humidity and temperature data to ThingsBoard
        client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)

        next_reading += INTERVAL
        sleep_time = next_reading-time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
            
            
except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()
