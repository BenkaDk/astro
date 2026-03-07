import json
from datetime import datetime

def log_event(event_name):
    print(f"Event logged: {event_name}")
    event = {
        "type": event_name,
        "timestamp": datetime.now().isoformat()
    }
    with open("game_events.jsonl", "a") as f:
        f.write(json.dumps(event) + "\n")
