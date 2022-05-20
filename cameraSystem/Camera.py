import RPi.GPIO as GPIO
#import asyncio
from time import sleep
from collections import deque

from tb_device_mqtt import TBDeviceMqttClient #, TBPublishInfo

POSITION_ZERO = [60, 90]

class Camera():
    def __init__(self):
        # Create a Queue where actions gimble actions will be stored before being carried out
        self.previousAction = ""
        #self.actionQueue = deque()
        #self.moveStatus = False

        # Set up MQTT Connection
        self.client = TBDeviceMqttClient("demo.thingsboard.io", "NmhyyW2DzT0Zb7C41PvS")
        
        # Connect to ThingsBoard
        self.client.connect()
        self.client.send_telemetry({"currentFirmwareVersion": 0.1})
        self.client.subscribe_to_attribute("command", self.parseCommand)

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
        # asyncio.run(self.turn(POSITION_ZERO))

        # Keep the Motors Quite
        self.sleepMotors()

    # Destructor
    def __del__(self):
        # Turn to face the user
        self.turn(POSITION_ZERO)
        # asyncio.run(self.turn(POSITION_ZERO))

        # Stop servos
        self.tiltServo.stop()
        self.panServo.stop()

        # Disconnect from MQTT
        self.client.disconnect()

        # Free GPIO
        GPIO.cleanup()

    def cameraGibleLoop(self):
        # As we can't subscribe to MQTT notifications with our version of ThingsBoard, we poll things board for updates to position. This also keeps the Python script alive
        while True:
            sleep(100)

    def parseCommand(self, client: TBDeviceMqttClient, content: dict[str, str], message: str):
        # Get command from message and split by space
        # If Command is Move, the command will have the format
            # [M, tiltValue, panValue]
        # If Command is Wait, the command will have the format
            # [W, waitTime]

        print(content)
            
        try:
            command = content.get('client').get('command').split(' ')
            
            if command[0] == 'm':
                if len(command) == 3:
                    try:
                        angle = list(map(float, command[1:3]))
                    except ValueError:
                        raise ValueError("Angle to move is not two floats or ints seperated by a comman\nm,63.1,90.2")
                    
                    self.turn(angle)
                    #self.actionQueue.append(lambda: self.turn(angle))
                    #await self.turn(angle)
                else:
                    raise ValueError("Angle to move is not two floats or ints seperated by a comma\nnm,63.1,90.2")
            elif command[0] == 'w':
                if len(command) == 2:
                    try:
                        waitTime = float(command[1])
                    except ValueError:
                        raise ValueError("Wait time is not a float or int\nw,10.1")
                    
                    self.wait(waitTime)
                    #self.actionQueue.append(lambda: self.wait(waitTime))
                    #await self.wait(waitTime)
                else:
                    raise ValueError("Wait time is not a float or int\nw,10.1")
            else:
                raise ValueError("Unknown command: Please use either m; move, or w; wait.\nm,63.1,90.2")
        except AttributeError:
            sleep(1) 

    def turn(self, angle: list[float]):
        # Don't allow new gimble actions to be carried out while we move it
        #self.moveStatus = True

        self.tiltServo.ChangeDutyCycle(2+(angle[0]/18))
        self.panServo.ChangeDutyCycle(2+(angle[1]/18))

        result = self.client.send_telemetry({"pan": angle[0], "tilt": angle[1]})
        #success = result.get() == TBPublishInfo.TB_ERR_SUCCESS

        # Allow the servo to move to position
        sleep(0.4)

        # Put the servos to sleep such that the gimble doesn't try to maintain position
        # If the gimble is told to maintain position it constantly moves due to the digital PWM wave outputted by the RPi, and the low quality of the servos being used
        self.sleepMotors()
        
        #self.moveStatus = False

    def sleepMotors(self):
        # Stop servos
        self.tiltServo.ChangeDutyCycle(0)
        self.panServo.ChangeDutyCycle(0)

    def wait(self, waitTime: float): 
        self.sleepMotors()
        sleep(waitTime)
        #await asyncio.sleep(waitTime)
    
if __name__ == "__main__":
    camera = Camera()
    camera.cameraGibleLoop()