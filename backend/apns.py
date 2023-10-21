import requests
import json
from settings import Settings
from aioapns import APNs, NotificationRequest, PushType
import asyncio

settings = Settings()

def get_apns_config() -> APNs:
	return APNs(
		key='config/key.p8',
		key_id=settings["APNS_KEY_ID"],
		team_id=settings["APNS_TEAM_ID"],
		topic=settings["APNS_TOPIC"],  # Bundle ID
		use_sandbox=True,
	)


async def send_apns_event(device_token : str, message : str):
	if not device_token:
		device_token = settings["TEST_DEVICE_TOKEN"]

	request = NotificationRequest(
		device_token=settings["TEST_DEVICE_TOKEN"],
		message = {
			"aps": {
				"type": "event",
				"message": message
			}
		},
	)
	await (get_apns_config()).send_notification(request)

async def send_apns_instruction(device_token : str, title : str, body : str):
	if not device_token:
		device_token = settings["TEST_DEVICE_TOKEN"]

	request = NotificationRequest(
		device_token=settings["TEST_DEVICE_TOKEN"],
		message = {
			"aps": {
				"type": "instruction",
				"title": title,
				"content": body,
			}
		},
	)
	await (get_apns_config()).send_notification(request)

async def main():
	await send_apns_event(False, "Close")
	await send_apns_instruction(False, "Test Title", "Test Body")

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())