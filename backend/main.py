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
from apns import send_apns_instruction, send_apns_event
from copy import deepcopy

_print = print

def print(x : str):
    curr_time = time.strftime("%H:%M:%S", time.localtime())
    _print(f"[{curr_time}] {x}")

@dataclass
class ChatGPTData:
    identifier : str
    filepath : str

class ServerStatus(Enum):
    INITIAL = 0             # Client has just connected
    INITIAL_WAITING = 1     # Client has just connected and screen recording; waiting 8 sec period now
    PROCESSING = 2          # Client is now under processing stage.

class SocketReceiver:
    # TODO: Build ChatGPT queue scheduler
    # TODO add portal to accept the question asked
    def __init__(self):
        self.user_identifier_to_status : dict[str, ServerStatus] = {}
        self.user_identifier_to_timestamp : dict[str, int] = {}
        self.user_identifier_to_is_running : dict[str, bool] = {}
        self.user_identifier_to_device_token : dict[str, str] = {}
        self.user_identifier_to_question : dict[str, str] = {}

        self.chat_gpt_handler : ChatGPTHandler = ChatGPTHandler()
        
        self.chat_gpt_schedule : list[ChatGPTData] = []
    
    def get_status(self, identifier : str) -> ServerStatus:
        if identifier in self.user_identifier_to_status:
            return self.user_identifier_to_status[identifier]
        
        return ServerStatus.INITIAL

    async def run_chat_gpt_scheduler(self) -> None:
        print(f"[INFO] Running scheduler")
        if len(self.chat_gpt_schedule) == 0:
            # time.sleep(1)
            # self.run_chat_gpt_scheduler()
            return
        
        item = self.chat_gpt_schedule[0]
        print(f"[INFO] Chat GPT scheduler running for {item.identifier}")
        # Run stuff on chat gpt
        response = self.chat_gpt_handler.chatgpt_response(
                        item.filepath, 
                        self.user_identifier_to_question[item.identifier]
                    )
        # Send it back to Apple device
        if response["status"] == "on":
            print(f"[INFO] Sending APNS instruction to {self.user_identifier_to_device_token[item.identifier]}")
            await send_apns_instruction(
                self.user_identifier_to_device_token[item.identifier],
                response["title"],
                response["content"]
            )
            print("[INFO] Sent APNS instruction")

            self.user_identifier_to_timestamp[item.identifier] = time.time()
            self.user_identifier_to_is_running[item.identifier] = False
        else:
            print(f"[INFO] Sending APNS instruction to {self.user_identifier_to_device_token[item.identifier]}")
            await send_apns_event(
                self.user_identifier_to_device_token[item.identifier],
                "close"
            )
            print("[INFO] Sent APNS instruction")
            del self.user_identifier_to_device_token[item.identifier]
            del self.user_identifier_to_is_running[item.identifier]
            del self.user_identifier_to_question[item.identifier]
            del self.user_identifier_to_timestamp[item.identifier]
            del self.user_identifier_to_status[item.identifier]

        os.remove(item.filepath)
        # Event done
        del self.chat_gpt_schedule[0]
        # self.run_chat_gpt_scheduler()


    async def video_receiver(self, websocket, path) -> None:
        async for message in websocket:
            frame_data = json.loads(message)
            with open("logs.txt", "a") as file:
                save_data = frame_data
                if "data" in frame_data:
                    save_data = deepcopy(frame_data)
                    del save_data["data"]

                file.write(json.dumps(save_data, indent=4) + "\n")

            identifier = frame_data["identifier"]

            if frame_data["type"] == "event":
                match frame_data["message"]:
                    case "start":
                        self.user_identifier_to_question[identifier] = frame_data["question"]
                        self.user_identifier_to_device_token[identifier] = frame_data["apnsDeviceToken"]
                        print(f"[INFO] Matched {identifier} to device token {frame_data['apnsDeviceToken']}")
                continue

            status = self.get_status(identifier)

            # This enforcees status "off"
            if not identifier in self.user_identifier_to_question:
                continue

            # If their data is already being processed, skip
            if self.user_identifier_to_is_running.get(identifier, False):
                continue

            match status:
                case ServerStatus.INITIAL:
                    self.user_identifier_to_timestamp[identifier] = time.time()
                    self.user_identifier_to_status[identifier] = ServerStatus.INITIAL_WAITING
                    continue

                case ServerStatus.INITIAL_WAITING:
                    time_diff = time.time() - self.user_identifier_to_timestamp[identifier]
                    if time_diff < 2:
                        continue

                    # Send in initial prompt data
                    self.user_identifier_to_is_running[identifier] = True
                    self.user_identifier_to_status[identifier] = ServerStatus.PROCESSING
                
                case ServerStatus.PROCESSING:
                    time_diff = time.time() - self.user_identifier_to_timestamp[identifier]
                    if (time.time() - self.user_identifier_to_timestamp[identifier] < 5):
                        continue

                    self.user_identifier_to_is_running[identifier] = True

            # Do processing here; frame is collected and message is sent based on that        
            timestamp = frame_data["timestamp"]
            frame_bytes = base64.b64decode(frame_data["data"])

            # Process the frame and its metadata
            filename = self.process_frame(self.user_identifier_to_device_token[identifier], timestamp, frame_bytes)

            data_object = ChatGPTData(
                identifier,
                filename
            )
            print(f"[INFO] {identifier}: added {filename}")
            self.chat_gpt_schedule.append(data_object)
            await self.run_chat_gpt_scheduler()
            print(f"[INFO] Scheduler end")
            # Process done. Let them go through next stage now.

    def process_frame(self, device_token, timestamp, frame_data) -> str:
        filename = f"{device_token}-{timestamp}.png"
        image = Image.open(io.BytesIO(frame_data))
        image.save(filename, 'PNG')
        return filename

async def run(receiver : SocketReceiver):
    async with websockets.serve(receiver.video_receiver, "localhost", 5678):
        await asyncio.Future()

receiver = SocketReceiver()

threading.Thread(
    target = asyncio.run(run(receiver))
).start()