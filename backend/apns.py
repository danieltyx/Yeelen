import requests
import json
import ssl

def push_notification(device_token : str, title : str, body : str):
    # Your alert data
    # alert_data = {
    #     "title": "Access Cellular Settings",
    #     "body": "Tap on the 'Cellular' option from the list to access cellular data settings."
    # }
    # You'll need to replace these with your own values
    device_token = "your_device_token"
    apns_topic = "your_app_bundle_id"
    apns_key_id = "your_apns_key_id"
    auth_token = "your_auth_token"  # generated JWT

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
