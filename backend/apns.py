import requests
import json
from settings import Settings
from aioapns import APNs, NotificationRequest, PushType
import asyncio

settings = Settings()

async def send_apns(device_token : str, title : str, body : str):
	if not device_token:
		device_token = settings["TEST_DEVICE_TOKEN"]

	apns_key_client = APNs(
		key='config/key.p8',
		key_id=settings["APNS_KEY_ID"],
		team_id=settings["APNS_TEAM_ID"],
		topic=settings["APNS_TOPIC"],  # Bundle ID
		use_sandbox=True,
	)
	request = NotificationRequest(
		device_token=settings["TEST_DEVICE_TOKEN"],
		message = {
			"aps": {
				"alert": "Hello from APNs",
				"badge": "1",
			}
		},
	)
	await apns_key_client.send_notification(request)

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(send_apns())