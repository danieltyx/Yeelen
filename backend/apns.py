import http.client
import json
import ssl

# Your alert data
alert_data = {
    "title": "Access Cellular Settings",
    "body": "Tap on the 'Cellular' option from the list to access cellular data settings."
}

# Create the notification payload
payload = {
    "aps": {
        "alert": alert_data,
        "sound": "default"
    },
    "status": "on"
}

# Convert the payload to a JSON string
payload_json = json.dumps(payload)

# Set up the HTTP/2 connection to APNs
context = ssl.create_default_context()
connection = http.client.HTTPSConnection("api.development.push.apple.com", 443, context=context)

# You'll need to replace these with your own values
device_token = "your_device_token"
apns_topic = "your_app_bundle_id"
apns_key_id = "your_apns_key_id"
auth_token = "your_auth_token"  # generated JWT

# Create the POST request
url = f"/3/device/{device_token}"
headers = {
    "apns-topic": apns_topic,
    "apns-key-id": apns_key_id,
    "authorization": f"bearer {auth_token}"
}

# Send the request
connection.request("POST", url, body=payload_json, headers=headers)

# Get the response
response = connection.getresponse()
print(f"Response status: {response.status}")
print(f"Response reason: {response.reason}")
print(f"Response data: {response.read().decode('utf-8')}")

# Close the connection
connection.close()
