# server.py
from flask import Flask, request, render_template
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
import json
import socket
import sqlite3

app = Flask(__name__)
app.config.from_object(__name__)
clients = {}

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/pipe")
def pipe():
    if request.environ.get("wsgi.websocket"):
        ws = request.environ["wsgi.websocket"]
        key = str(ws)
        clients[key] = ws
        print(key,"add")
        try:
            while True:
                msg = ws.receive()
                d=json.loads(msg)

              
                for client in clients.values():
                    client.send(d['text'])
        except:
            ws.close()
            del clients[key]
            print(key,"del")
    else:
        return

def main():
    app.debug = True
    host=socket.gethostname()
    ip = socket.gethostbyname(host)


    server = pywsgi.WSGIServer((ip, 8080), app, handler_class=WebSocketHandler)

    server.serve_forever()


if __name__ == "__main__":
    main()
   
