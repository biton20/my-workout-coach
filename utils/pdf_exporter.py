from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def export_workout_to_pdf(workout, filename="my_workout.pdf", user_name="User"):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Logo (optional)
    logo_path = "logo.png"
    if os.path.exists(logo_path):
        c.drawImage(logo_path, x=width - 120, y=height - 100, width=60, height=60)

    # Title
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, height - 50, "🔥 Your Personalized Workout Plan")

    # User info
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"Name: {user_name}")
    c.drawString(50, height - 120, f"Date: {datetime.today().strftime('%d/%m/%Y')}")
    c.line(50, height - 130, width - 50, height - 130)

    # Workout content
    y = height - 160
    for i, ex in enumerate(workout, 1):
        if "sets" in ex:
            line = f"{i}. {ex['name']} — {ex['sets']} x {ex['reps']} reps (equipment: {ex['equipment']})"
        elif "duration" in ex:
            line = f"{i}. {ex['name']} — Duration: {ex['duration']} sec (equipment: {ex['equipment']})"
        else:
            line = f"{i}. {ex['name']}"  # CrossFit or generic exercise
        c.drawString(50, y, line)
        y -= 25
        if y < 50:
            c.showPage()
            y = height - 50

    c.save()
    return filename

