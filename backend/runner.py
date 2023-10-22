import firebase_admin
from firebase_admin import credentials, firestore
import subprocess
import sys
import re

COMMAND = "cloudflared tunnel --url http://localhost:5678"

cred = credentials.Certificate("config/firebase.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

cloudflared = db.collection('links').document('cloudflared')

def set_url(url : str):
    cloudflared.set(
        {
            "url": url
        }
    )

def get_url() -> str:
    return cloudflared.get().to_dict()["url"]

with subprocess.Popen(COMMAND, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as process:
    for line in process.stdout:
        line = line.decode('utf-8')
        print(line, end = "")

        line_search = re.search(r'(https://)+.+(.trycloudflare.com)+', line)
        if not line_search:
            continue

        set_url(str(line_search[0]).replace("https://", "ws://"))