dani-howard@dani-howard-IdeaPad-Slim-3-15IRH8:~/personal-development-ai$ cd ~/personal-development-ai
dani-howard@dani-howard-IdeaPad-Slim-3-15IRH8:~/personal-development-ai$ git status
On branch main
Your branch is up to date with 'origin/main'.

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	api.py
	requirements.txt

nothing added to commit but untracked files present (use "git add" to track)
dani-howard@dani-howard-IdeaPad-Slim-3-15IRH8:~/personal-development-ai$ 

# Personal Development AI

> **Work in Progress**

## Project Goal

Personal Development AI is a learning and portfolio project focused on building an adaptive habit progression system.

The application allows a user to define a duration-based habit, record daily performance, and receive an adjusted target for the following week.

The project combines a Python machine-learning backend with a simple web interface.

## Current Version

The current prototype includes:

- weekly habit tracking
- daily planned and actual duration tracking
- synthetic user data generation
- a machine-learning model for predicting weekly completion rates
- a rule-based progression recommender
- a FastAPI backend
- an HTML/CSS/JavaScript frontend
- communication between the frontend and Python backend through an API

The project is still under development.

## How It Works

1. The user enters a habit and a target duration.
2. A weekly table is created for recording daily performance.
3. The user enters the actual duration completed each day.
4. At the end of the week, the frontend sends the week's data to the FastAPI backend.
5. The backend calculates weekly performance.
6. The system determines the target duration for the following week.
7. The frontend displays the new target and creates the next week's tracking table.

## Machine Learning

The `CompletionPredictor` uses a Random Forest Regressor from scikit-learn.

Because real user data is not yet available, the model is currently trained using synthetic behavioral data.

The training data includes features such as:

- planned duration
- final duration goal
- previous weekly readiness values

The model predicts the expected weekly completion rate.

The model is evaluated using a train/test split and Mean Absolute Error (MAE), and the trained model is saved using `joblib`.

## Progression Recommender

The project also contains a rule-based `ProgressionRecommender`.

It uses the predicted completion rate to determine how the planned duration should change.

The current progression rules are:

- below 50% predicted completion → decrease target by 10%
- 50%–70% → keep the same target
- 70%–85% → increase target by 5%
- above 85% → increase target by 10%

This rule-based approach is intentionally simple and may be improved as the project develops.

## Synthetic Data

Synthetic user behavior is generated to develop and test the machine-learning pipeline before real user data is available.

The simulation includes variation in factors such as:

- base readiness
- habit goals
- weekly conditions
- daily performance
- planned duration

The synthetic data is intended for development and experimentation rather than as a replacement for real behavioral data.

## Web Application

The frontend is built with:

- HTML
- CSS
- JavaScript

The backend is built with:

- Python
- FastAPI

When the user finishes a week, JavaScript sends the weekly data to the `/finish-week` API endpoint.

The backend processes the data and returns information including the weekly readiness and next recommended duration. The frontend then displays the recommendation and creates the next week's table.

## Project Structure

```text
personal-development-ai/
├── api.py
├── main.py
├── train_model.py
├── ml_models.py
├── simulation.py
├── habit.py
├── dataset_builder.py
├── completion_predictor.joblib
├── requirements.txt
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── README.md
└── .gitignore
```

## Running the Project

Create and activate a virtual environment, then install the required dependencies:

```bash
pip install -r requirements.txt
```

Start the web application with:

```bash
python -m uvicorn api:app --reload
```

Then open:

```text
http://127.0.0.1:8000
```

## Technologies

- Python
- scikit-learn
- FastAPI
- joblib
- HTML
- CSS
- JavaScript
- Git / GitHub

## Development Status

This project is currently in progress.

The current version demonstrates an end-to-end flow from user input in the browser to Python backend processing and generation of the following week's habit target.

Future development may include improving the recommendation logic, testing with more realistic data, and expanding the application beyond the current prototype.