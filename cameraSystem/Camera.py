import RPi.GPIO as GPIO
from time import sleep

from tb_device_mqtt import TBDeviceMqttClient
import paho.mqtt.client as mqtt

POSITION_ZERO = [60, 90]

class Camera():
    def __init__(self):
        # Set up MQTT Connection
        self.tbClient = TBDeviceMqttClient("demo.thingsboard.io", "qSPi2bDBvBJaPJwcFrTX")
        self.moClient = mqtt.Client("gimbal")
        
        # Connect to MQTT
        self.tbClient.connect()
        self.moClient.connect("test.mosquitto.org")
        self.tbClient.send_telemetry({"currentFirmwareVersion": 0.1})
        self.moClient.subscribe("joystick/command")
        self.moClient.on_message = self.parseCommand

        # Reference GPIO pins with Broadcom SOC channel numbers
        GPIO.setmode(GPIO.BCM)

        # Initilise servo control pins
        GPIO.setup(18, GPIO.OUT)
        GPIO.setup(23,GPIO.OUT)
        self.tiltServo = GPIO.PWM(18, 50) # pin 18 for pan servo
        self.panServo = GPIO.PWM(23, 50) # pin 23 for tilt servo

        # Start PWM running on both servos, value of 0 (pulse off)
        self.tiltServo.start(0)
        self.panServo.start(0)

        # Turn to face the user
        self.turn(POSITION_ZERO)

    # Destructor
    def __del__(self):
        # Turn to face the user
        self.turn(POSITION_ZERO)

        # Stop servos
        self.tiltServo.stop()
        self.panServo.stop()

        # Disconnect from MQTT
        self.tbClient.disconnect()
        self.moClient.loop_stop()

        # Free GPIO
        GPIO.cleanup()

    def cameraGimbleLoop(self):
        # As we can't subscribe to MQTT notifications with our version of ThingsBoard, we use mosquitto as a subscribable MQTT broker.
        self.moClient.loop_start()

        while True:
            # This loop keeps the Python script alive 
            sleep(100)

    def parseCommand(self, client, userdata: dict[str, str], message: str):
        # Get command from message and split by space
        # If Command is Move, the command will have the format
            # [M, tiltValue, panValue]
        # If Command is Wait, the command will have the format
            # [W, waitTime]
            
        try:
            command = message.payload.decode("utf-8").split(' ')
            
            if command[0] == 'm':
                if len(command) == 3:
                    try:
                        angle = list(map(float, command[1:3]))
                    except ValueError:
                        raise ValueError("Angle to move is not two floats or ints seperated by a comma")
                    
                    self.turn(angle)
                else:
                    raise ValueError("Angle to move is not two floats or ints seperated by a comma")
            elif command[0] == 'w':
                if len(command) == 2:
                    try:
                        waitTime = float(command[1])
                    except ValueError:
                        raise ValueError("Wait time is not a float or int")
                    
                    self.wait(waitTime)
                else:
                    raise ValueError("Wait time is not a float or int")
            else:
                raise ValueError("Unknown command: Please use either m; move, or w; wait.")
        except AttributeError:
            print("Dropped a message")
            sleep(1) 

    def turn(self, angle: list[float]):
        self.tiltServo.ChangeDutyCycle(2+(angle[0]/18))
        self.panServo.ChangeDutyCycle(2+(angle[1]/18))

        result = self.tbClient.send_telemetry({"pan": angle[0], "tilt": angle[1]})

        # Put the servos to sleep such that the gimble doesn't try to maintain position
        # If the gimble is told to maintain position it constantly moves due to the digital PWM wave outputted by the RPi, and the low quality of the servos being used
        self.sleepMotors()

    def sleepMotors(self):
        # Stop servos
        self.tiltServo.ChangeDutyCycle(0)
        self.panServo.ChangeDutyCycle(0)

    def wait(self, waitTime: float): 
        self.sleepMotors()
        sleep(waitTime)
    
if __name__ == "__main__":
    camera = Camera()
    camera.cameraGimbleLoop()