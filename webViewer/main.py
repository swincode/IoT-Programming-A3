
import asyncio, time
import json
from tb_device_mqtt import TBDeviceMqttClient

from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# client = TBDeviceMqttClient("localhost", "bLvC1TSknBYefPXQFOSX")
client = TBDeviceMqttClient("demo.thingsboard.io", "NmhyyW2DzT0Zb7C41PvS")

# client = TBDeviceMqttClient("demo.thingsboard.io", "bLvC1TSknBYefPXQFOSX")
client.connect()
something = ""

@app.on_event("startup")
async def startup():
    print("Starting...")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    # camera_active = client.request_attributes(["camera_active"])
    return templates.TemplateResponse("home.html", {"request": request})

@app.websocket_route("/ws/controller")
async def websocket(websocket: WebSocket):
    await websocket.accept()
    while True:
        await asyncio.sleep(0.5)
        # Get mqtt to receive data

        def anon_inner(client, result, exception):
            data = result.get("client").get("command").split(" ")
            something = {
                        "x" : data[1],
                        "y" : data[2]
                    }
            return something
        data = client.request_attributes(["command"], callback=anon_inner)
        # return await websocket.send(data_return)
        # await websocket.send_text(data)

@app.get("/controller-data")
def controller_data():
    def get_data(client, result, error):
        print("there")
        data = result.get("client").get("command").split(" ")
        return PlainTextResponse(data)
    client.request_attributes(["command"], callback=get_data)
    time.sleep(3)

            

@app.websocket_route("/ws/control")
async def control_websocket(websocket: WebSocket):
    await websocket.accept()
    while True:
        txt = await websocket.receive_text()
        client.request_attributes(["command"], callback=send_update)
        def send_update(client, result, exception):
            print("callback")
            # match txt:
            #     case "toggle":
            #         client.send_attributes({"controller state" : not (result.get("client").get("controller state"))})
            #     case "up":
            #         client.send_attributes
            #     case "down":
            #     case "left":
            #     case "right":

@app.websocket_route("/ws/camera")
async def graph_websocket(websocket: WebSocket):
    await websocket.accept()
    while True:
        print("camera")     

def on_attributes_change(object, result, exception):
    if exception is not None:
        pass
        # print("Exception:", str(exception))
    else:
        try:
            data_return = result
        except Exception as e:
            print(e)    