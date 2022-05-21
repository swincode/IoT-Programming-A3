import paho.mqtt.client as mqtt
class DataController:
    def __init__(self, name:str):
        self.moClient = mqtt.Client(name)
        self.moClient.connect("test.mosquitto.org")
        self.moClient.subscribe("joystick/command")
        self.moClient.on_message = self.get_msg

        self.x_pos = 0
        self.y_pos = 0
        self.joystick_state = True
        self.send_data("joystick/enable", self.joystick_state)

    
    def __del__(self):
        self.moClient.loop_stop()
        self.moClient.disconnect()

    def get_msg(self, client, userdata, message: str) -> None:
        data = message.payload.decode("utf-8").split(" ")
        self.x_pos = data[1]
        self.y_pos = data[2]

    def get_data(self) -> None:
        return {"x":self.x_pos, "y":self.y_pos}
    
    def send_data(self, location: str, message: str) -> None:
        self.moClient.publish(location, str(message))

    def toggle_joystick_state(self):
        self.joystick_state = not self.joystick_state

