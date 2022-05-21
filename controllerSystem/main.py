
import serial

import paho.mqtt.client as mqtt
from tb_device_mqtt import TBDeviceMqttClient

ser = serial.Serial("/dev/ttyACM0", 9600)
disabled = False


tbClient = TBDeviceMqttClient("demo.thingsboard.io", "NmhyyW2DzT0Zb7C41PvS")
moClient = mqtt.Client("joystick")
tbClient.connect()
moClient.connect("test.mosquitto.org")
moClient.subscribe("joystick/disabled")

def disabled_state(client, userdata, message):
    print("here")
    disabled = bool(message.payload.decode("utf-8"))
    tbClient.send_attributes({"enabled" : disabled})

moClient.on_message = disabled_state

def main():
    state = True
    while True:
        if not disabled:
            data = parse_serial_input()
            if data == "toggle power":
                state = not state
                tbClient.send_attributes({"power state": state})
                moClient.publish("joystick/power", state)
            data_arr = data.split(",")
            if len(data_arr) == 2:
                data_arr[0] = int(data_arr[0]) - 30
                if int(data_arr[0]) < 0:
                    data_arr[0] = 0
                if int(data_arr[1]) < 0:
                    data_arr[1] = 0
                mqtt_string = f"m {data_arr[0]} {data_arr[1]}"
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
