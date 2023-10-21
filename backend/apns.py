import requests
import json
from settings import Settings
from aioapns import APNs, NotificationRequest, PushType
import asyncio

settings = Settings()
def push_notification(device_token : str, title : str, body : str):
    # Your alert data
    # alert_data = {
    #     "title": "Access Cellular Settings",
    #     "body": "Tap on the 'Cellular' option from the list to access cellular data settings."
    # }
    # You'll need to replace these with your own values
    apns_topic = settings["APNS_BUNDLE_ID"]
    apns_key_id = settings["APNS_KEY_ID"]
    auth_token = settings["APNS_AUTH_TOKEN"]

    alert_data = {
        "title": title,
        "body": body
    }
    payload = {
        "aps": {
            "alert": alert_data,
            "sound": "default"
        },
        "status": "on"
    }
    payload_json = json.dumps(payload)
    headers = {
        "apns-push-type": "alert",
        "authorization": f"bearer {auth_token}"
    }
    requests.post(
        f"api.sandbox.push.apple.com:443/3/device/{device_token}",
        json = payload_json,
        headers = headers
    )

async def send_apns():
    apns_key_client = APNs(
        key='/path/to/apns-key.p8',
        key_id='<KEY_ID>',
        team_id='<TEAM_ID>',
        topic='<APNS_TOPIC>',  # Bundle ID
        use_sandbox=False,
    )
    request = NotificationRequest(
        device_token='<DEVICE_TOKEN>',
        message = {
            "aps": {
                "alert": "Hello from APNs",
                "badge": "1",
            }
        },
        notification_id=str(uuid4()),  # optional
        time_to_live=3,                # optional
        push_type=PushType.ALERT,      # optional
    )
    await apns_cert_client.send_notification(request)
    await apns_key_client.send_notification(request)
