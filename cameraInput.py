from Camera import Camera

camera = Camera()

while True:
    camera.turn([int(i) for i in input("Enter tilt, pan values: ").split(',')])