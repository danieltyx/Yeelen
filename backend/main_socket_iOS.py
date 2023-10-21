import asyncio
import websockets
import json
import base64
from PIL import Image
import io
import os
from enum import Enum
import time
from gpt import ChatGPTHandler
import threading
from dataclasses import dataclass

@dataclass
class ChatGPTData:
    identifier : str
    filepath : str
    question : str

class ServerStatus(Enum):
    INITIAL = 0             # Client has just connected
    INITIAL_WAITING = 1     # Client has just connected and screen recording; waiting 8 sec period now
    PROCESSING = 2          # Client is now under processing stage.

class SocketReceiver:
    # TODO: Build ChatGPT queue scheduler
    # TODO add portal to accept the question asked
    def __init__(self):
        self.user_states : dict[str, ServerStatus] = {}
        self.user_to_timestamp : dict[str, int] = {}
        self.user_is_running : dict[str, bool] = {}
        self.chat_gpt_handler : ChatGPTHandler = ChatGPTHandler()
        
        self.chat_gpt_scheduler : list[ChatGPTData] = []
    
    def get_status(self, identifier : str) -> ServerStatus:
        if identifier in self.user_states:
            return self.user_states[identifier]
        
        return ServerStatus.INITIAL

    def chat_gpt_scheduler(self) -> None:
        if len(self.chat_gpt_scheduler) == 0:
            self.chat_gpt_scheduler()
            time.sleep(1)
            return
        
        item = self.chat_gpt_scheduler[0]
        # Run stuff on chat gpt
        response = ChatGPTHandler.chatgpt_response(item.filepath, item.question) 
        # TODO: Send in notification here from apns.py
        # Send it back to Apple device
        del self.chat_gpt_scheduler[0]
        self.chat_gpt_scheduler()

    async def video_receiver(self, websocket, path):
        async for message in websocket:
            # TO DO: add identifier as appropriate
            identifier = "EST"
            status = self.get_status(identifier)

            # If their data is already being processed, skip
            if identifier in self.user_is_running and self.user_is_running[identifier]:
                continue

            match status:
                case ServerStatus.INITIAL:
                    self.user_to_timestamp[identifier] = time.time()
                    self.user_states[identifier] = ServerStatus.INITIAL_WAITING
                    continue

                case ServerStatus.INITIAL_WAITING:
                    time_diff = time.time() - self.user_to_timestamp[identifier]
                    if time_diff < 8:
                        continue

                    # Send in initial prompt data
                    self.user_is_running[identifier] = True
                    self.user_states[identifier] = ServerStatus.PROCESSING
                
                case ServerStatus.PROCESSING:
                    time_diff = time.time() - self.user_to_timestamp[identifier]
                    if (time.time() - self.user_to_timestamp[identifier] < 4):
                        continue

                    self.user_is_running[identifier] = True

            # Do processing here; frame is collected and message is sent based on that        
            frame_data = json.loads(message)
            timestamp = frame_data["timestamp"]
            frame_bytes = base64.b64decode(frame_data["data"])

            # Process the frame and its metadata
            filename = self.process_frame(timestamp, frame_bytes)

            data_object = ChatGPTData(
                identifier,
                filename,
                "Question" # TODO: get question from the frontend
            )
            self.chat_gpt_scheduler.append(data_object)
            # Process done. Let them go through next stage now.
            self.user_to_timestamp[identifier] = time.time()
            self.user_is_running[identifier] = False

    def process_frame(self, timestamp, frame_data) -> str:
        print(timestamp)
        filename = os.path.join(r"C:\Users\anubh\OneDrive\Documents\UMich Documents\Classes\MATH 395\test", str(timestamp) + ".png")
        image = Image.open(io.BytesIO(frame_data))
        image.save(filename, 'PNG')
        print("Saved")
        return filename

async def run(receiver):
    async with websockets.serve(receiver.video_receiver, "localhost", 5678):
        await asyncio.Future()

receiver = SocketReceiver()

threading.Thread(
    target = asyncio.run(run(receiver))
).run()

threading.Thread(
    target = receiver.chat_gpt_scheduler()
).run()