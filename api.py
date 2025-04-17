from fastapi import FastAPI
from coach.generator import generate_workout
from fastapi.responses import FileResponse
from utils.pdf_exporter import export_workout_to_pdf

app = FastAPI()

@app.get("/")
def root():
    return {"message": "ברוכים הבאים ל-My Workout Coach API"}

@app.get("/generate")
def get_workout(goal: str = "strength", equipment: str = "none", duration: int = 20):
    workout = generate_workout(goal, equipment, duration)
    return {"workout": workout}

@app.get("/generate/pdf")
def get_workout_pdf(goal: str = "strength", equipment: str = "none", duration: int = 20, name: str = "User"):
    workout = generate_workout(goal, equipment, duration)
    export_workout_to_pdf(workout, filename="my_workout.pdf", user_name=name)
    return FileResponse("my_workout.pdf", media_type="application/pdf", filename="my_workout.pdf")
