from pathlib import Path

import joblib

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from habit import DailyAttempt, Habit
from ml_models import ProgressionRecommender


app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent

predictor = joblib.load(
    BASE_DIR / "completion_predictor.joblib"
)

recommender = ProgressionRecommender()

DAYS = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday"
]


class WeekData(BaseModel):
    week_number: int
    planned_duration: float
    duration_goal: float
    actual_durations: list[float]
    last_week_readiness: float | None = None


@app.post("/finish-week")
def finish_week(data: WeekData):

    if len(data.actual_durations) != 7:
        raise HTTPException(
            status_code=400,
            detail="Exactly 7 daily durations are required."
        )

    habit = Habit(
        "Current Habit",
        data.duration_goal
    )

    completed_days = 0

    for day, actual_duration in zip(
        DAYS,
        data.actual_durations
    ):

        attempt = DailyAttempt(
            day,
            data.planned_duration,
            actual_duration
        )

        habit.add_attempt(attempt)

        if actual_duration >= data.planned_duration:
            completed_days += 1


    weekly_readiness = (
        habit.calculate_weekly_readiness()
    )

    weekly_completion_rate = (
        completed_days / 7
    )


    if data.week_number == 1:

        next_duration = round(
            weekly_readiness * data.duration_goal
        )

        predicted_completion = None

    else:

        features = [[
            data.planned_duration,
            data.duration_goal,
            weekly_readiness,
            data.last_week_readiness
        ]]

        predicted_completion = float(
            predictor.predict(features)[0]
        )

        progression = (
            recommender.progression_calculation(
                predicted_completion
            )
        )

        next_duration = round(
            data.planned_duration * progression
        )

        next_duration = min(
            next_duration,
            data.duration_goal
        )


    return {
        "weekly_readiness": weekly_readiness,
        "weekly_completion_rate": weekly_completion_rate,
        "predicted_completion": predicted_completion,
        "next_duration": next_duration
    }


app.mount(
    "/",
    StaticFiles(
        directory=BASE_DIR / "frontend",
        html=True
    ),
    name="frontend"
)