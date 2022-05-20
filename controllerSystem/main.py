
import serial

from tb_device_mqtt import TBDeviceMqttClient, TBPublishInfo

ser = serial.Serial("/dev/ttyACM0", 9600)

client = TBDeviceMqttClient("demo.thingsboard.io", "NmhyyW2DzT0Zb7C41PvS")
# client = TBDeviceMqttClient("localhost", "token")
client.connect()

def main():
    state = True
    while True:
        
        data = parse_serial_input()
        if data == "toggle power":
            state = not state
            client.send_attributes({"power state": state})
        data_arr = data.split(",")
        if len(data_arr) == 2:
            mqtt_struct = {
                "command" : f"m {data_arr[0]} {data_arr[1]}" 
            }
            telemetry = {
                "position" : f"{data_arr[0]},{data_arr[1]}"
            }
            client.send_attributes(mqtt_struct)
            client.send_telemetry(telemetry)
        
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
