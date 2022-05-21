
import random
from time import sleep
import paho.mqtt.client as mqtt

flag = False

class DataController:
    def __init__(self, name:str):
        self.moClient = mqtt.Client(name)
        self.moClient.connect("test.mosquitto.org")
        self.moClient.subscribe("joystick/command")
        self.moClient.on_message = self.get_msg

        self.x_pos = 0
        self.y_pos = 0
    
    def __del__(self):
        self.moClient.loop_stop()
        self.moClient.disconnect()

    def get_msg(self, client, userdata, message: str) -> None:
        data = message.payload.decode("utf-8").split(" ")
        self.x_pos = data[1]
        self.y_pos = data[2]

    def get_data(self) -> None:
        return {"x":self.x_pos, "y":self.y_pos}
    
    def send_data(self, message: str) -> None:
        self.moClient.publish("joystick/command", message)

try:
    if flag:
        cli = mqtt.Client("joystick")
        cli.connect("test.mosquitto.org")
        data_controller = DataController()
        data_controller.moClient.loop_start()
        while True:
            sleep(1)
            print("sending")
            cli.publish("joystick/command", f"m {random.randint(0, 180)} {random.randint(0, 180)}")
except KeyboardInterrupt:
    pass