from flask import Blueprint, jsonify, request
from flask_cors import CORS
from app.webhook.models import format_push, format_pull_request, format_merge
from app.extensions import collection
import pytz

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')
CORS(webhook)

@webhook.route('/')
def hello_world():
    return 'Hello World'


@webhook.route('/receiver', methods=['POST'])
def receiver():
    data = request.json
    event = request.headers.get('X-GitHub-Event')

    if event == 'push':
        formatted = format_push(data)
    elif event == 'pull_request':
        action = data.get("action")
        if action == "opened":
            formatted = format_pull_request(data)
        elif action == "closed" and data["pull_request"].get("merged"):
            formatted = format_merge(data)
        else:
            return jsonify({"msg": "ignored"}), 200
    else:
        return jsonify({"msg": "ignored"}), 200

    collection.insert_one(formatted)
    return jsonify({"msg": "received"}), 200

@webhook.route('/events', methods=['GET'])
def get_events():
    ist = pytz.timezone('Asia/Kolkata')  # Set target local timezone
    events = list(collection.find({}, {'_id': 0}).sort("timestamp", -1).limit(10))

    for e in events:
        utc_time = e["timestamp"].replace(tzinfo=pytz.utc)  # Make sure it's timezone-aware
        local_time = utc_time.astimezone(ist)
        e["timestamp"] = local_time.strftime('%d %B %Y - %I:%M %p IST')  # Format in IST

    return jsonify(events)
