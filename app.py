import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from coach.generator import generate_custom_workout
from utils.pdf_exporter import export_workout_to_pdf
from utils.history import save_to_history, load_history

st.set_page_config(page_title="My Workout Coach", layout="centered")

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .stButton>button {
            color: white;
            background-color: #1f77b4;
            border-radius: 0.5rem;
        }
        .stDownloadButton>button {
            background-color: #2ca02c;
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🏋️ My Workout Coach")
st.write("Create a personalized workout based on your goals, equipment, and intensity.")

with st.form("workout_form"):
    name = st.text_input("Your name", "User")
    goal = st.selectbox("Workout goal", ["strength", "cardio", "crossfit"])
    equipment = st.multiselect(
        "Available equipment",
        ["none", "dumbbells", "barbell", "machine", "bike"],
        default=["none"]
    )
    intensity = st.selectbox("Intensity", ["easy", "medium", "hard"])
    num_exercises = st.slider("How many exercises?", 1, 10, 3)

    muscle_group = None
    if goal == "strength":
        muscle_group = st.selectbox("Target muscle group", ["chest", "legs", "back", "full_body"])

    submitted = st.form_submit_button("Generate Workout")

if submitted:
    workout = generate_custom_workout(goal, equipment, muscle_group, num_exercises, intensity)

    st.subheader(f"{name}'s Workout Plan ({intensity.capitalize()})")

    if workout and isinstance(workout, list) and "name" in workout[0]:
        if "sets" in workout[0]:
            df = pd.DataFrame([
                {"Exercise": ex["name"], "Sets": ex["sets"], "Reps": ex["reps"], "Equipment": ex["equipment"]}
                for ex in workout
            ])
        elif "duration" in workout[0]:
            df = pd.DataFrame([
                {"Exercise": ex["name"], "Duration (sec)": ex["duration"], "Equipment": ex["equipment"]}
                for ex in workout
            ])
        else:
            df = pd.DataFrame([{"Exercise": ex["name"]} for ex in workout])

        st.dataframe(df, use_container_width=True)
        save_to_history(name, goal, intensity, workout)

        filename = export_workout_to_pdf(workout, user_name=name)
        with open(filename, "rb") as f:
            pdf_data = f.read()

        st.download_button(
            label="📄 Download as PDF",
            data=pdf_data,
            file_name=filename,
            mime="application/pdf"
        )
    else:
        st.warning("No suitable exercises found. Please change your options.")

with st.expander("📜 View My Workout History"):
    history = load_history()
    if not history:
        st.info("No workout history found.")
    else:
        for item in reversed(history[-5:]):
            st.write(f"**{item['user']}** | {item['goal']} | {item['intensity']} | {item['timestamp'][:16]}")
            for i, ex in enumerate(item['workout'], 1):
                if "sets" in ex:
                    st.markdown(f"- {i}. {ex['name']} — {ex['sets']} x {ex['reps']} reps")
                elif "duration" in ex:
                    st.markdown(f"- {i}. {ex['name']} — {ex['duration']} seconds")
                else:
                    st.markdown(f"- {i}. {ex['name']}")
            st.markdown("---")

        st.markdown("### 📈 Intensity Distribution")
        df_hist = pd.DataFrame(history)
        df_hist["timestamp"] = pd.to_datetime(df_hist["timestamp"])
        counts = df_hist["intensity"].value_counts()
        fig, ax = plt.subplots()
        counts.plot(kind="bar", ax=ax, color=["green", "orange", "red"])
        ax.set_ylabel("Sessions")
        ax.set_xlabel("Intensity Level")
        st.pyplot(fig)