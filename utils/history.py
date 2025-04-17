import json
from datetime import datetime
import os

HISTORY_FILE = "workout_history.json"

def save_to_history(user_name, goal, intensity, workout):
    entry = {
        "user": user_name,
        "goal": goal,
        "intensity": intensity,
        "timestamp": datetime.now().isoformat(),
        "workout": workout
    }

    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(entry)

    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []
