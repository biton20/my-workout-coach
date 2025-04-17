from coach.generator import generate_custom_workout
from utils.pdf_exporter import export_workout_to_pdf
from utils.history import save_to_history

def main():
    print("🏋️ Welcome to My Workout Coach!")

    # קלט מהמשתמש
    user_name = input("What's your name? ").strip()
    goal = input("Choose your goal (strength/cardio): ").strip().lower()

    muscle_group = None
    if goal == "strength":
        muscle_group = input("Choose muscle group (chest/legs/back/full_body): ").strip().lower()

    equipment = input("Available equipment? (none/dumbbells/barbell): ").strip().lower()
    intensity = input("Choose intensity (easy/medium/hard): ").strip().lower()
    num_exercises = int(input("How many exercises do you want? "))

    # יצירת האימון
    workout = generate_custom_workout(
        goal=goal,
        equipment=equipment,
        muscle_group=muscle_group,
        num_exercises=num_exercises,
        intensity=intensity
    )

    # הדפסת האימון
    print(f"\n🔥 {user_name}, here is your workout plan ({intensity.capitalize()}):")
    for i, ex in enumerate(workout, 1):
        if goal == "strength":
            print(f"{i}. {ex['name']} - {ex['sets']} sets x {ex['reps']} reps (equipment: {ex['equipment']})")
        else:
            print(f"{i}. {ex['name']} - {ex['duration']} seconds (equipment: {ex['equipment']})")

    # שמירה להיסטוריה
    save_to_history(user_name, goal, intensity, workout)

    # שמירה כ־PDF
    save_pdf = input("\nDo you want to save your workout as a PDF? (y/n): ").strip().lower()
    if save_pdf == "y":
        export_workout_to_pdf(workout, user_name=user_name)
        print("📄 Workout saved as 'my_workout.pdf'")

if __name__ == "__main__":
    main()
