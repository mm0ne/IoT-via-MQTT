import eventlet
import json
from flask import Flask, render_template, request
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from db import create_instance
from supabase.client import Client

eventlet.monkey_patch()

db: Client = create_instance()

app = Flask(__name__, template_folder="./templates")
app.config["SECRET"] = "my secret key"
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["MQTT_BROKER_URL"] = "192.168.237.94"
app.config["MQTT_BROKER_PORT"] = 1883
app.config["MQTT_USERNAME"] = ""
app.config["MQTT_PASSWORD"] = ""
app.config["MQTT_KEEPALIVE"] = 60
app.config["MQTT_TLS_ENABLED"] = False

mqtt = Mqtt(app)
socketio = SocketIO(app)


@app.route("/", methods=["GET"])
def index():
    mqtt.unsubscribe_all()
    mqtt.subscribe("mobilan")

    floor = 1
    if request.args.get("floor"):
        floor = int(request.args.get("floor"))

    response = db.table("mobilan").select("*").filter("floor", "eq", str(floor)).limit(10).execute()
    return render_template("./index.html", data=response.data)


@socketio.on("publish")
def handle_publish(json_str):
    data = json.loads(json_str)
    mqtt.publish(data["topic"], data["message"])


@socketio.on("subscribe")
def handle_subscribe(json_str):
    data = json.loads(json_str)
    mqtt.subscribe(data["topic"])


@socketio.on("unsubscribe_all")
def handle_unsubscribe_all():
    mqtt.unsubscribe_all()


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    list_message = message.payload.decode().split("|")
    list_message = [i.split(",") for i in list_message]
    list_message = [
        {"floor": j + 1, "lamp_is_on": i[0] == "1", "fan_is_on": i[1] == "1"} for j, i in enumerate(list_message)
    ]

    response = db.table("mobilan").insert(list_message).execute()
    data = dict(topic=message.topic, payload=response.data)
    socketio.emit("mqtt_message", data=data)


@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, use_reloader=True, debug=True)