from flask import Flask
from flask_sock import Sock
import json
import threading

app = Flask(__name__)
sock = Sock(app)

clients = []


@sock.route("/ws")
def websocket(ws):
    clients.append(ws)

    print("Client connected!")

    try:
        while True:
            message = ws.receive()

            if message is None:
                break

            data = json.loads(message)
            print("Client:", data)

    finally:
        clients.remove(ws)
        print("Client disconnected!")


def server_input():
    while True:
        message = input("Server > ")

        data = {
            "type": "server_message",
            "message": message
        }

        for ws in clients:
            try:
                ws.send(json.dumps(data))
            except:
                pass


threading.Thread(target=server_input, daemon=True).start()

app.run(debug=True, port=1928)
