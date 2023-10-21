import requests
import json
from settings import Settings

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
        "apns-topic": apns_topic,
        "apns-key-id": apns_key_id,
        "authorization": f"bearer {auth_token}"
    }
    requests.post(
        f"api.development.push.apple.com:443/3/device/{device_token}",
        json = payload_json,
        headers = headers
    )
