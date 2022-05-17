import RPi.GPIO as GPIO

class Camera:
    def __init__(self):
        # Reference GPIO pins with Broadcom SOC channel numbers
        GPIO.setmode(GPIO.BCM)

        # Initilise servo control pins
        GPIO.setup(18, GPIO.OUT)
        GPIO.setup(23,GPIO.OUT)
        self.panServo = GPIO.PWM(18,50) # pin 18 for pan servo
        self.tiltServo = GPIO.PWM(23,50) # pin 23 for tilt servo

        # Start PWM running on both servos, value of 0 (pulse off)
        self.panServo.start(0)
        self.tiltServo.start(0)

        # Turn to face the user
        self.turn([60, 0])

    # Destructor
    def __del__(self):
        # Stop servos
        self.panServo.stop()
        self.tiltServo.stop()

        # Free GPIO
        GPIO.cleanup()

    def turn(self, angle: list[float]):
        self.panServo.ChangeDutyCycle(2+(angle[0] /18))
        self.tiltServo.ChangeDutyCycle(2+(angle[1]/18))

    