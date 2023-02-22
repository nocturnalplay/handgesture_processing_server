from handGesture import hand
import cv2
import mediapipe as mp
from data import serverData as env
from websockets import serve
import asyncio
import sys
import json

async def Handler(websocket):
    print("waiting for the client messgae")
    message = json.loads(await websocket.recv())
    try:
        if message["event"] == "video":
            get_video_output()
        elif message["event"] == "frame":
            get_frame_output()
            
    except KeyboardInterrupt:
        print("Force exit operation")
        sys.exit()

try:
    async def main():
        print(f"server created on {env.PORT} port")
        async with serve(Handler, env.HOST, env.PORT, ping_interval=None):
            await asyncio.Future()  # run forever
    asyncio.run(main())

except KeyboardInterrupt:
    print("Force exit operation")
    sys.exit()
