
import paho.mqtt.client as mqtt
from tb_device_mqtt import TBDeviceMqttClient

class DataController:
    def __init__(self, name:str):

        self.tbClient = TBDeviceMqttClient("demo.thingsboard.io", "NmhyyW2DzT0Zb7C41PvS")
        self.tbClient.connect()


        self.moClient = mqtt.Client(name)
        self.moClient.connect("test.mosquitto.org")
        self.moClient.subscribe("joystick/state")
        self.moClient.on_message = self.get_msg

        self.joystick_state = True
        #self.send_data("joystick/state", f"joystick {self.joystick_state}")

    
    def __del__(self):
        self.moClient.loop_stop()
        self.moClient.disconnect()

    def get_msg(self, client, userdata, message: str) -> None:
        # data = message.payload.decode("utf-8")
        stringRep = message.payload.decode("utf-8")
        self.tbClient.send_attributes({"enabled" : stringRep})
        if stringRep == "True":
            self.joystick_state = True
        else:
            self.joystick_state = False

    def get_data(self) -> None:
        return str(self.joystick_state)
    
    def send_data(self, location: str, message: str) -> None:
        self.moClient.publish(location, str(message))

    def toggle_joystick_state(self):
        self.joystick_state = not self.joystick_state

    def send_attributes(self, attributes: dict):
        self.tbClient.send_attributes(attributes)

