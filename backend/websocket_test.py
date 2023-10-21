from websocket import create_connection
ws = create_connection("ws://happening-bubble-birthday-headlines.trycloudflare.com")
ws.send("Hello, World")
print("WOO")