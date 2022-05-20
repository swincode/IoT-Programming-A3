
import asyncio, time
import json
from tb_device_mqtt import TBDeviceMqttClient

from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        something = controller_data()
        await websocket.send_json(json.dumps(something))
        
        # return await websocket.send(data_return)
        # await websocket.send_text(data)

def controller_data():
    def get_data(client, result, error):
        print("there")
        if result != None:
            data = result.get("client").get("command").split(" ")
            json_resp = {
                "command" : data[0],
                "x" : data[1],
                "y" : data[2]
            }
            return json_resp
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