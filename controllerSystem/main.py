
import serial

import paho.mqtt.client as mqtt

from DataController import DataController

class ControllerSystem:
    def __init__(self):
        self.ser = serial.Serial("/dev/ttyACM0", 9600)
        self.sendData = True
        self.powerState = True
        
        self.data_controller = DataController("joystick")
        self.data_controller.moClient.loop_start()

    def main(self):
        while True:
            if self.data_controller.joystick_state:
                data = self.parse_serial_input()
                if data == "toggle power":
                    self.powerState = not self.powerState
                    self.data_controller.send_attributes({"power state": self.powerState})
                    self.data_controller.send_data("joystick/power", f"irrigation {self.powerState}")
                data_arr = data.split(",")
                if len(data_arr) == 2:
                    mqtt_string = f"m {data_arr[0]} {data_arr[1]}"
                    self.data_controller.send_data("joystick/command", mqtt_string)
                    mqtt_struct = {
                        "command" : mqtt_string 
                    }
                    self.data_controller.send_attributes(mqtt_struct)

                print(data_arr)
            else:
                print("off")

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
