import RPi.GPIO as GPIO
import asyncio

from ..controllerSystem.mqtt import MQTT_Connection

class Camera():
    def __init__(self):
        # Reference GPIO pins with Broadcom SOC channel numbers
        GPIO.setmode(GPIO.BCM)

        # Initilise servo control pins
        GPIO.setup(18, GPIO.OUT)
        GPIO.setup(23,GPIO.OUT)
        self.panServo = GPIO.PWM(18, 50) # pin 18 for pan servo
        self.tiltServo = GPIO.PWM(23, 50) # pin 23 for tilt servo

        # Start PWM running on both servos, value of 0 (pulse off)
        self.panServo.start(0)
        self.tiltServo.start(0)

        # Turn to face the user
        self.turn([60, 0])

        # Set up MQTT Connection
        self.connection = MQTT_Connection(broker="172.20.10.6", token="vzAaa8tPs5w59UxPVBDR")

    # Destructor
    def __del__(self):
        # Turn to face the user
        self.turn([60, 0])

        # Stop servos
        self.panServo.stop()
        self.tiltServo.stop()

        # Free GPIO
        GPIO.cleanup()

    # async def waitForCommand(self, MQTTConnection: MQTTConnection):
        # while True:
            # await parseCommand(mqttCommand)

    async def waitForCommand(self):
        while True:
            await self.parseCommand(input("Enter command: "))

    async def parseCommand(self, mqttCommand: str): 
        brokenCommand = mqttCommand.split(',')
        if brokenCommand[0] == 'm':
            if len(brokenCommand) == 3:
                try:
                    angle = list(map(float, brokenCommand[1:3]))
                except ValueError:
                    raise ValueError("Angle to move is not two floats or ints seperated by a comman\nm,63.1,90.2")
                self.turn(angle)
            else:
                raise ValueError("Angle to move is not two floats or ints seperated by a comma\nnm,63.1,90.2")
        elif brokenCommand[0] == 'w':
            if len(brokenCommand) == 2:
                try:
                    waitTime = float(brokenCommand[1])
                except ValueError:
                    raise ValueError("Wait time is not a float or int\nw,10.1")
                await self.wait(waitTime)
            else:
                raise ValueError("Wait time is not a float or int\nw,10.1")
        else:
            raise ValueError("Unknown command: Please use either m; move, or w; wait.\nm,63.1,90.2")


    def turn(self, angle: list[float]):
        self.panServo.ChangeDutyCycle(2+(angle[0] /18))
        self.tiltServo.ChangeDutyCycle(2+(angle[1]/18))

    async def wait(self, waitTime: float): 
        # Stop servos
        self.panServo.ChangeDutyCycle(0)
        self.tiltServo.ChangeDutyCycle(0)

        await asyncio.sleep(waitTime)
    
if __name__ == "__main__":
    camera = Camera()
    asyncio.run(camera.waitForCommand())