
import json
import paho.mqtt.client as mqtt

# Free cloud broker, uncomment for use
# mqttBroker = "test.mosquitto.org"

class MQTT_Connection:
    def __init__(self, broker="localhost", port=1883, timeout=60, telemetry_location="v1/devices/me/telemetry", token="token"):

        self.client = mqtt.Client()
        self.telemetry_location = telemetry_location

        self.client.on_connect = self.on_connect
        self.client.on_connect_fail = self.on_connect_fail
        self.client.on_message = self.get_message

        self.client.username_pw_set(token)
        self.client.connect(broker, port, timeout)
        self.client.loop()

    def __del__(self):
        self.client.disconnect()
        
    def get_message(self, client, userdata, message):
        return str(message.payload.decode("utf-8"))
    
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc) :
        if (rc==0) :
            print("connected OK Returned code = ", rc)
            self.post_message(10, 5)
        else :
            print("Bad connection Returned code = ", rc)
    
    def on_connect_fail(self):
        print("connection failed")

    def post_message(self, struct) -> None:
        self.client.publish(self.telemetry_location, json.dumps(struct), 1)



