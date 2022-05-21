import random
from time import sleep
import paho.mqtt.client as mqtt

flag = True

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
    
    def send_data(self, message: str) -> None:
        self.moClient.publish("joystick/power", message)

data_controller = DataController("irrigation")
data_controller.moClient.loop_start()
       