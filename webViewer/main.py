
import json
from time import sleep

from tb_device_mqtt import TBDeviceMqttClient

from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

client = TBDeviceMqttClient("localhost", "token")
# client = TBDeviceMqttClient("demo.thingsboard.io", "bLvC1TSknBYefPXQFOSX")
client.connect()

@app.on_event("startup")
async def startup():
    print("Starting...")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.websocket_route("/ws/data")
async def websocket(websocket: WebSocket):
    await websocket.accept()
    while True:
        # Get mqtt to receive data
        positions = client.request_attributes(["x", "y"], callback=on_attributes_change)
        return await websocket.send(positions)

@app.websocket_route("/ws/camera")
async def graph_websocket(websocket: WebSocket):
    await websocket.accept()
    while True:
        print("camera")     

def on_attributes_change(object, result, exception):
    if exception is not None:
        print("Exception:", str(exception))
    else:
        return result
    