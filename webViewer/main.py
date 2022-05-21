import asyncio
import json

from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from DataController import DataController

app = FastAPI(host="0.0.0.0")

templates = Jinja2Templates(directory="templates")

data_controller = DataController("website")

@app.on_event("startup")
async def startup():
    data_controller.moClient.loop_start()
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
        data = data_controller.get_data()
        # print(data)
        try:
            await websocket.send_json(json.dumps(data))
        except Exception as e:
            print(e)
        
        # return await websocket.send(data_return)
        # await websocket.send_text(data)            

@app.websocket_route("/ws/position")
async def control_websocket(websocket: WebSocket):
    await websocket.accept()
    while True:
        txt = await websocket.receive_text()
        result = data_controller.get_data()
        match txt:
            case "toggle":
                data_controller.toggle_joystick_state()
                data_controller.send_data("joystick/disabled", data_controller.joystick_state)
            case "up":
                result["x"] = int(result["x"]) - 20
            case "down":
                result["x"] = int(result["x"]) + 20
            case "left":
                result["y"] = int(result["y"]) + 20
            case "right":
                result["y"] = int(result["y"]) - 20
        data_controller.send_data("joystick/command", f"m {result['x']} {result['y']}")   

def on_attributes_change(object, result, exception):
    if exception is not None:
        pass
        # print("Exception:", str(exception))
    else:
        try:
            data_return = result
        except Exception as e:
            print(e)    