import serial

import paho.mqtt.client as mqtt
from tb_device_mqtt import TBDeviceMqttClient

ser = serial.Serial("/dev/ttyACM0", 9600)

tbClient = TBDeviceMqttClient("demo.thingsboard.io", "qSPi2bDBvBJaPJwcFrTX")
moClient = mqtt.Client("joystick")
tbClient.connect()
moClient.connect("test.mosquitto.org")

def main():
    while True:
        data = parse_serial_input()
        data_arr = data.split(",")
        if len(data_arr) == 2:
            data_arr[0] -= 30
            if data_arr[0] < 0:
                data_arr[0] = 0
            mqtt_string = f"m {data_arr} {data_arr[1]}"
            moClient.publish("joystick/command", mqtt_string)
            mqtt_struct = {
                "command" : mqtt_string 
            }
            tbClient.send_attributes(mqtt_struct)
        print(data_arr)

def parse_serial_input() -> str:
        """
        Return a string representation of binary data
        """
        bin_input = str(ser.readline().rstrip()).replace('b', '').replace("'", "")
        return bin_input

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
