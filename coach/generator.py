import random
from coach.data import strength_exercises, cardio_exercises, crossfit_exercises

def adjust_difficulty(ex, intensity, goal):
    if goal == "strength":
        factor = {"easy": 0.8, "medium": 1.0, "hard": 1.2}[intensity]
        ex["sets"] = max(1, round(ex["sets"] * factor))
        ex["reps"] = max(1, round(ex["reps"] * factor))
    elif goal == "cardio":
        factor = {"easy": 0.8, "medium": 1.0, "hard": 1.3}[intensity]
        ex["duration"] = max(10, round(ex["duration"] * factor))
    return ex

def generate_custom_workout(goal, equipment, muscle_group=None, num_exercises=3, intensity="medium"):
    workout = []

    if isinstance(equipment, str):
        equipment = [equipment]

    if goal == "cardio":
        filtered = [ex for ex in cardio_exercises if ex["equipment"] in equipment or ex["equipment"] == "none"]
        if not filtered:
            return [{"name": "No cardio exercises available with your equipment."}]
        workout = random.sample(filtered, min(num_exercises, len(filtered)))

    elif goal == "strength":
        if muscle_group == "full_body":
            all_exercises = []
            for group in ["chest", "back", "legs"]:
                all_exercises.extend(strength_exercises[group])
        else:
            all_exercises = strength_exercises.get(muscle_group, [])

        filtered = [ex for ex in all_exercises if ex["equipment"] in equipment or ex["equipment"] == "none"]

        if not filtered:
            return [{"name": "No strength exercises available with your equipment."}]

        random.shuffle(filtered)
        workout = filtered[:num_exercises]

    elif goal == "crossfit":
        filtered = [ex for ex in crossfit_exercises if ex["equipment"] in equipment or ex["equipment"] == "none"]
        if not filtered:
            return [{"name": "No crossfit exercises available with your equipment."}]
        workout = random.sample(filtered, min(num_exercises, len(filtered)))

    workout = [adjust_difficulty(ex.copy(), intensity, goal) for ex in workout]
    return workout
