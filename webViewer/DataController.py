import paho.mqtt.client as mqtt
class DataController:
    def __init__(self, name:str):
        self.moClient = mqtt.Client(name)
        self.moClient.connect("test.mosquitto.org")
        self.moClient.subscribe([("joystick/command", 0), ("joystick/state", 0), ("joystick/power", 0)])
        self.moClient.on_message = self.get_msg

        self.x_pos = 0
        self.y_pos = 0
        self.joystick_state = True
        self.irrigation_state = False
        self.send_data("joystick/state", f"joystick {self.joystick_state}")

    
    def __del__(self):
        self.moClient.loop_stop()
        self.moClient.disconnect()

    def get_msg(self, client, userdata, message: str) -> None:
        data = message.payload.decode("utf-8").split(" ")
        print(data)
        if len(data) == 3:
            self.x_pos = data[1]
            self.y_pos = data[2]
        else:
            if data[0] == "joystick":
                if data[1] == "True":
                    self.joystick_state = True
                else:
                    self.joystick_state = False
            else:
                if data[1] == "True":
                    self.irrigation_state = True
                else:
                    self.irrigation_state = False

    def get_data(self) -> None:
        return {"x":self.x_pos, "y":self.y_pos, "state":self.joystick_state, "irrigation":self.irrigation_state}
    
    def send_data(self, location: str, message: str) -> None:
        self.moClient.publish(location, str(message))

    def toggle_joystick_state(self):
        self.joystick_state = not self.joystick_state
    
    def toggle_irrigation_state(self):
        self.irrigation_state = not self.irrigation_state

