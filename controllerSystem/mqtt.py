
import paho.mqtt.client as mqtt

mqttBroker = "localhost"
token = "testing"

# Free cloud broker, uncomment for use
# mqttBroker = "test.mosquitto.org"

class MQTT_Connection:
    def __init__(self):
        self.client = mqtt.Client()
        
        self.client.on_connect = self.on_connect
        self.client.on_connect_fail = self.on_connect_fail
        self.client.on_message = self.get_message

        self.client.username_pw_set(token)
        self.client.connect(mqttBroker)
        
    def get_message(client, userdata, message):
        return str(message.payload.decode("utf-8"))
    
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc) :
        if (rc==0) :
            print("connected OK Returned code = ", rc)
        else :
            print("Bad connection Returned code = ", rc)
    
    def on_connect_fail():
        print("connection failed")

    def post_message(self, x:int, y: int) -> None:
        self.client.publish("position", x, y)

mqtt = MQTT_Connection()
mqtt.post_message(5, 5)

