import joblib

from ml_models import CompletionPredictor, ProgressionRecommender
from simulation import SyntheticDataGenerator
from habit import DailyAttempt, Habit

WEEKS = 10

DAYS = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday"
]


generator = SyntheticDataGenerator() # creates the object that generates synthetic user behaviour

predictor = joblib.load("completion_predictor.joblib")
recommender = ProgressionRecommender() # creates the rule-based recommender


habit_name, duration_goal = generator.create_habit()

base_readiness = generator.create_base_readiness()


habit = Habit(habit_name, duration_goal) # create the Habit object

planned_duration = duration_goal # initial value

previous_planned_duration = None

last_week_readiness = None
two_weeks_ago_readiness = None


for week in range(1, WEEKS+1):

    print()
    print("Week:", week)
    print("Planned duration:", planned_duration)

    completed_days = 0 # how many days were completed this week

    weekly_condition = generator.create_weekly_condition()

    for day in DAYS:

        actual_duration = generator.generate_actual_duration(
            planned_duration,
            duration_goal,
            base_readiness,
            weekly_condition, 
            planned_duration
            )

        completion = int(actual_duration >= planned_duration) # 0 or 1

        completed_days += completion # adds to the weekly counter

        attempt = DailyAttempt(day, planned_duration, actual_duration) # this day's attempt

        habit.add_attempt(attempt) # stores the attempt inside the Habit object

    weekly_completion_rate = (completed_days / len(DAYS)) # what precentage of the 7 days were completed

    weekly_readiness = habit.calculate_weekly_readiness()

    print("Actual completionrade:", round(weekly_completion_rate,2))

    print("Weekly readiness:", round(weekly_readiness, 2))


    # For the ML model
    if week==1:

        next_duration = round(weekly_readiness * duration_goal) # calibaration

    elif(last_week_readiness is None or two_weeks_ago_readiness is None): # not enough history

        next_duration = planned_duration # stay the same

    else:

        features = [[
            planned_duration,
            duration_goal,
            weekly_readiness,
            last_week_readiness
            ]] # create the feature vector for the ML model in the same order used during training

        predicted_completion = predictor.predict(features)[0] # predicts the expected completion rate for the next week

        progression = recommender.progression_calculation(predicted_completion) # uses the pridection to choose a progression multiplier

        next_duration = planned_duration * progression # next week's planned duration

        next_duration = min(next_duration, duration_goal) # upper bound

        next_duration = max(next_duration,0) # lower bound

        next_duration = round(next_duration)

        print("Predicted next-week completion:", round(predicted_completion, 2))

        print("Progression multiplier:", progression)


    # Shift the readiness history forward

    two_weeks_ago_readiness = last_week_readiness

    last_week_readiness = weekly_readiness

    previous_planned_duration = planned_duration

    planned_duration = next_duration