# Personal Development AI

**Dani Howard**

> **Work in Progress**

## Project Goal

Personal Development AI is a learning and portfolio project focused on building an adaptive habit progression system.

The current prototype allows users to define a duration-based habit, track daily performance, and adjust future targets using machine-learning predictions and progression rules.

## Development Approach

This project is being developed iteratively.

I use AI-assisted development tools for learning unfamiliar technologies, debugging, code review, and exploring design alternatives while implementing, testing, and refining the project logic myself.

## Current Version

The current prototype focuses on adaptive habit progression.

Users define a habit and target duration, record their daily performance, and receive an adjusted target for the following week.

At this stage, the project includes:

- weekly progress tracking
- synthetic user data for development
- a machine-learning model that predicts weekly completion rates
- a rule-based progression recommender
- an HTML/CSS/JavaScript interface

## How It Works

1. The user chooses a habit and target duration.
2. The user records the actual duration completed each day.
3. At the end of the week, the system calculates weekly performance.
4. A machine-learning model predicts the expected completion rate.
5. The progression recommender uses that prediction to adjust the next week's planned duration.
6. The process repeats each week.

## Machine Learning

The current `CompletionPredictor` uses a Random Forest Regressor from scikit-learn.

The model is trained using synthetic behavioral data because real user data is not yet available.

Current model inputs include:

- planned duration
- final duration goal
- previous week's readiness
- readiness from two weeks earlier

The model predicts the expected weekly completion rate.

The trained model is evaluated using a train/test split and Mean Absolute Error (MAE).

## Progression Recommender

The `ProgressionRecommender` currently uses a rule-based approach.

Based on the predicted completion rate, it chooses a progression multiplier:

- below 50% → decrease target by 10%
- 50%–70% → keep the same target
- 70%–85% → increase target by 5%
- above 85% → increase target by 10%

The recommender is intentionally simple at this stage.

## Synthetic Data

To develop the ML pipeline before real user data is available, the project generates simulated user behavior.

Synthetic users currently vary by factors such as:

- base readiness
- goal difficulty
- weekly conditions
- day-to-day variation
- changes in planned duration

The synthetic-data system is used as a development and testing environment, not as a substitute for real behavioral data.

## Web Interface

The frontend is being developed with:

- HTML
- CSS
- JavaScript

The interface currently allows the user to:

- enter a habit and target duration
- generate a weekly tracking table
- record actual duration for each day
- complete a week and continue to the next weekly section

The Finish Week button sends the seven daily durations to FastAPI's
`POST /finish-week` endpoint. Week 1 calibrates the next target from readiness;
later weeks use the saved `CompletionPredictor` and `ProgressionRecommender`.
The returned target populates the next weekly table, and readiness is carried
forward for the next request. Failed requests leave the week available to retry.

### Run the web app

From the repository root, with your Python environment activated:

```bash
pip install fastapi uvicorn scikit-learn joblib
uvicorn api:app --reload
```

Open http://127.0.0.1:8000. FastAPI serves both the frontend and API; do not
open the HTML directly or use a separate static server. The existing
`completion_predictor.joblib` must be present in the repository root.
Progress is held in the page's memory and resets on reload or when creating
a new habit. No database is used.

## Project Structure

```text
personal-development-ai/
├── main.py
├── api.py
├── train_model.py
├── ml_models.py
├── simulation.py
├── habit.py
├── dataset_builder.py
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── README.md
└── .gitignore
```
