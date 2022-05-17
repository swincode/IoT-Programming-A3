
import json
import paho.mqtt.client as mqtt

# Free cloud broker, uncomment for use
# mqttBroker = "test.mosquitto.org"

class MQTT_Connection:
    def __init__(self, broker:str="localhost", port:int=1883, timeout:int=60, telemetry_location:str="v1/devices/me/telemetry", token:str="token") -> None:

        self.client = mqtt.Client()
        self.telemetry_location = telemetry_location

        self.client.on_connect = self.on_connect
        self.client.on_connect_fail = self.on_connect_fail
        self.client.on_message = self.get_message

        self.client.username_pw_set(token)
        self.client.connect(broker, port, timeout)
        self.client.loop_start()

    def __del__(self) -> None:
        self.client.disconnect()

    def subcribe_to(self, subscription: str) -> None:
        self.client.subscribe(subscription)
        
    def get_message(self, client, userdata, message) -> str:
        return str(message.payload.decode("utf-8"))
    
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc) -> None:
        if (rc==0) :
            print("connected OK Returned code = ", rc)
        else :
            print("Bad connection Returned code = ", rc)
    
    def on_connect_fail(self) -> None:
        print("connection failed")

    def post_message(self, struct) -> None:
        self.client.publish(self.telemetry_location, json.dumps(struct), 1)

