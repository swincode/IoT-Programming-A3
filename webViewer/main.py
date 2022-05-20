
import asyncio
from tb_device_mqtt import TBDeviceMqttClient

from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# client = TBDeviceMqttClient("localhost", "bLvC1TSknBYefPXQFOSX")
client = TBDeviceMqttClient("demo.thingsboard.io", "NmhyyW2DzT0Zb7C41PvS")

# client = TBDeviceMqttClient("demo.thingsboard.io", "bLvC1TSknBYefPXQFOSX")
client.connect()

@app.on_event("startup")
async def startup():
    print("Starting...")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    # camera_active = client.request_attributes(["camera_active"])
    return templates.TemplateResponse("home.html", {"request": request})

@app.websocket_route("/ws/data")
async def websocket(websocket: WebSocket):
    await websocket.accept()
    while True:
        await asyncio.sleep(0.5)
        # Get mqtt to receive data
        def anon_inner(client, result, exception):
            print(result)
            
        client.request_attributes(["command"], callback=anon_inner)
        # return await websocket.send(data_return)

@app.websocket_route("/ws/control")
async def control_websocket(websocket: WebSocket):
    await websocket.accept()
    while True:
        txt = await websocket.receive_text()
        print(txt)

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