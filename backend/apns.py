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
		device_token=device_token,
		message = {
			"aps": {
				"content-available": 1
				#"alert": "Yeelen",
			},
			"type": "event",
			"message": message
		},
		push_type=PushType.BACKGROUND
	)
	await (get_apns_config()).send_notification(request)

async def send_apns_instruction(device_token : str, title : str, body : str):
	if not device_token:
		device_token = settings["TEST_DEVICE_TOKEN"]

	request = NotificationRequest(
		device_token=device_token,
		message = {
			"aps": {
				"interruption-level": "time-sensitive",
				"alert": {
					"title": title,
					"body": body
				}
			},
		},
		push_type=PushType.ALERT
	)
	await (get_apns_config()).send_notification(request)

async def main():
	await send_apns_event("7d8b3a24cd5827c583367c1037ed6821ed2a0592931b8908a1c256f2ad5a7a46", "Close")
	#await send_apns_instruction("7d8b3a24cd5827c583367c1037ed6821ed2a0592931b8908a1c256f2ad5a7a46", "Test Title", "Test Body")

if __name__ == "__main__":
	asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
	asyncio.run(main())