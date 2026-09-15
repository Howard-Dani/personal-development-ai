# Personal Development AI

**Dani Howard**

> **Work in Progress**

## Project Goal

The long-term goal is to build an AI-assisted personal development and behavioral goal platform that helps users define goals, build routines, track progress, and adapt their plans over time.

The current version focuses on one part of that larger idea: building and adapting duration-based habits using user progress and machine-learning predictions.

## Development Approach

This project is being developed iteratively as a learning and portfolio project.

I use AI-assisted development tools for learning unfamiliar technologies, debugging, code review, and exploring design alternatives while implementing, testing, and refining the project logic myself.

## Current Version

The current prototype focuses on adaptive habit progression. Users define a habit and a target duration, track their daily performance, and receive an adjusted target for the following week.

At this stage, the project includes weekly progress tracking, synthetic user data for development, a machine-learning model that predicts completion rates, a rule-based progression recommender, and an HTML/CSS/JavaScript interface.

## How It Works

The current system follows this flow:

1. The user chooses a habit and target duration.
2. The user records the actual duration completed each day.
3. At the end of the week, the system calculates weekly performance.
4. A machine-learning model predicts the expected completion rate.
5. The progression recommender uses that prediction to adjust the next week's planned duration.
6. The process repeats each week.

## Machine Learning

The current `CompletionPredictor` uses a Random Forest Regressor from scikit-learn.

The model is currently trained using synthetic behavioral data because real user data is not yet available.

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

The recommender is intentionally simple at this stage. A future version may learn the progression policy from real user data.

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

The frontend is currently being developed with:

- HTML
- CSS
- JavaScript

The interface allows the user to enter a habit and target duration, then creates a weekly tracking table for recording the actual duration completed each day.

At the end of each week, the system is designed to use the recorded progress to calculate and display the recommended target for the following week. New weekly tables can then be added as the user continues tracking progress.

## Project Structure

```text
personal-development-ai/
├── main.py
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