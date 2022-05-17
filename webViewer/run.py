
from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
async def startup():
    print("Starting...")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.websocket_route("/ws/position")
async def websocket(websocket: WebSocket):
    await websocket.accept()
    while True:
        # Get mqtt to receive data
        print("todo")

@app.websocket_route("/ws/camera")
async def graph_websocket(websocket: WebSocket):
    await websocket.accept()
    while True:
        print("camera")     

