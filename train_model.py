from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib

from ml_models import CompletionPredictor
from simulation import SyntheticDataGenerator
from habit import DailyAttempt, Habit


USERS = 500
WEEKS = 10
PRECENTAGE = 0.1

DAYS = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday"
]


generator = SyntheticDataGenerator()

X = []
y = []


for user_id in range(1, USERS + 1):

    habit_name, duration_goal = generator.create_habit()
    base_readiness = generator.create_base_readiness()

    habit = Habit(habit_name, duration_goal)

    planned_duration = duration_goal

    previous_planned_duration = None
    last_week_readiness = None
    two_weeks_ago_readiness = None

    first_week = True


    for week in range(1, WEEKS + 1):

        completed_days = 0

        use_for_ml = (
            last_week_readiness is not None
            and two_weeks_ago_readiness is not None
        )

        if use_for_ml:
            X.append([
                planned_duration,
                duration_goal,
                last_week_readiness,
                two_weeks_ago_readiness
            ])

        weekly_condition = generator.create_weekly_condition()

        for day in DAYS:

            actual_duration = generator.generate_actual_duration(
                planned_duration,
                duration_goal,
                base_readiness,
                weekly_condition,
                previous_planned_duration
            )

            completion = int(
                actual_duration >= planned_duration
            )

            completed_days += completion

            attempt = DailyAttempt(
                day,
                planned_duration,
                actual_duration
            )

            habit.add_attempt(attempt)


        weekly_completion_rate = (
            completed_days / len(DAYS)
        )

        weekly_readiness = (
            habit.calculate_weekly_readiness()
        )


        if use_for_ml:
            y.append(weekly_completion_rate)


        current_planned_duration = planned_duration

        # Baseline progression rule used only to generate historical data
        if first_week:

            planned_duration = weekly_readiness * duration_goal

            first_week = False

        elif weekly_readiness < last_week_readiness:

            planned_duration -= PRECENTAGE * duration_goal

            planned_duration = max(
                planned_duration,
                0
            )

        else:

            planned_duration += PRECENTAGE * duration_goal

            planned_duration = min(
                planned_duration,
                duration_goal
            )


        planned_duration = round(planned_duration)

        previous_planned_duration = current_planned_duration


        # Move readiness history forward
        two_weeks_ago_readiness = last_week_readiness

        last_week_readiness = weekly_readiness


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
) # split the generated dataset


# Train the model
predictor = CompletionPredictor()

predictor.train(
    X_train,
    y_train
)


# Evaluate it
predictions = predictor.predict(X_test)

mae = mean_absolute_error(
    y_test,
    predictions
)

print("MAE:", mae)


joblib.dump(
    predictor,
    "completion_predictor.joblib"
) # save the trained predictor

print("Model saved.")