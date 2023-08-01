# main.py
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import socketio
import uvicorn

app = FastAPI()
sio = socketio.AsyncServer()
socket_app = socketio.ASGIApp(sio, app)

# HTML content for the chat room
chat_room_html = """
<!-- index.html -->
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta http-equiv="X-UA-Compatible" content="ie=edge" />
    <title>Document</title>
  </head>
  <body>
    <button onClick="sendMsg()">Hit Me</button>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/2.2.0/socket.io.js"></script>
    <script>
      const socket = io("http://localhost:8080");

      function sendMsg() {
        socket.emit("message", "HELLO WORLD");
      }
    </script>
  </body>
</html>
"""

new_chat_room_html = """"""
@app.get("/", response_class=HTMLResponse)
async def get_chat_room():
    return new_chat_room_html


# @sio.on("connect")
# async def connect(sid, environ):
#     print(f"Client connected: {sid}")


# @sio.on("disconnect")
# async def disconnect(sid):
#     print(f"Client disconnected: {sid}")


# @sio.on("send_message")
# async def handle_message(sid, message):
#     print(f"Received message: {message}")
#     await sio.emit("message", message, room=sid)

if __name__ == "__main__":
    
    uvicorn.run("main:app", host="localhost", port=8000)
