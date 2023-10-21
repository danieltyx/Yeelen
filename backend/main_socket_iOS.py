import asyncio
import websockets
import json
import base64
from PIL import Image
import io
import os

async def video_receiver(websocket, path):
    async for message in websocket:
        frame_data = json.loads(message)
        timestamp = frame_data["timestamp"]
        frame_bytes = base64.b64decode(frame_data["data"])

        # Process the frame and its metadata
        process_frame(timestamp, frame_bytes)

def process_frame(timestamp, frame_data):
    # Your frame processing logic
    print(timestamp)
    filename = os.path.join("/Users/zhuhaoyu/Downloads/stream", str(timestamp) + ".png")
    image = Image.open(io.BytesIO(frame_data))
    image.save(filename, 'PNG')
    print("Saved")



loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

start_server = websockets.serve(video_receiver, "172.20.10.3", 5678)

loop.run_until_complete(start_server)
loop.run_forever()