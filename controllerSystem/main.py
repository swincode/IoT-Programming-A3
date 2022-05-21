
import serial

import paho.mqtt.client as mqtt
from tb_device_mqtt import TBDeviceMqttClient

class ControllerSystem:
    def __init__(self):
        self.ser = serial.Serial("/dev/ttyACM0", 9600)
        self.sendData = True
        self.powerState = True

        self.tbClient = TBDeviceMqttClient("demo.thingsboard.io", "NmhyyW2DzT0Zb7C41PvS")
        self.moClient = mqtt.Client("joystick")
        self.tbClient.connect()
        self.moClient.connect("test.mosquitto.org")
        self.moClient.subscribe("joystick/state")

        self.moClient.on_message = self.disabled_state

    def disabled_state(self, client, userdata, message):
        print("here")
        stringRep = message.payload.decode("utf-8")
        self.tbClient.send_attributes({"enabled" : stringRep})
        if stringRep == "True":
            self.sendData = True
        else:
            self.sendData = False

    def main(self):
        while True:
            if self.sendData:
                data = self.parse_serial_input()
                if data == "toggle power":
                    self.powerState = not self.powerState
                    self.tbClient.send_attributes({"power state": self.powerState})
                    self.moClient.publish("joystick/power", self.powerState)
                data_arr = data.split(",")
                if len(data_arr) == 2:
                    data_arr[0] = int(data_arr[0]) - 30
                    if int(data_arr[0]) < 0:
                        data_arr[0] = 0
                    if int(data_arr[1]) < 0:
                        data_arr[1] = 0
                    mqtt_string = f"m {data_arr[0]} {data_arr[1]}"
                    self.moClient.publish("joystick/command", mqtt_string)
                    mqtt_struct = {
                        "command" : mqtt_string 
                    }
                    self.tbClient.send_attributes(mqtt_struct)

                print(data_arr)

    def parse_serial_input(self) -> str:
            """
            Return a string representation of binary data
            """
            bin_input = str(self.ser.readline().rstrip()).replace('b', '').replace("'", "")
            return bin_input

if __name__ == "__main__":
    try:
        controllerSystem = ControllerSystem()
        controllerSystem.main()
    except KeyboardInterrupt:
        pass
