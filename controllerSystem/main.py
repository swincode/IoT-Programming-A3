
import serial
from mqtt import MQTT_Connection

ser = serial.Serial("/dev/ttyACM0", 9600)

mqtt = MQTT_Connection()

def main():
    while True:
        data = parse_serial_input()
        data_arr = data.split(",")
        if len(data_arr) == 2:
            mqtt.post_message(data_arr[0], data_arr[1])

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