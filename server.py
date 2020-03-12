# server.py
from flask import Flask, request, render_template
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

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
                for client in clients.values():
                    client.send(msg)
        except:
            ws.close()
            del clients[key]
            print(key,"del")
    else:
        print("a")
        return("abc")

def main():
    app.debug = True
    server = pywsgi.WSGIServer(("", 8080), app, handler_class=WebSocketHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
