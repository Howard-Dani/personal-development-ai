from ml_models import CompletionPredictor
from simulation import SyntheticDataGenerator
from dataset_builder import DatasetBuilder
from habit import DailyAttempt, Habit

USERS = 10 
WEEKS = 10 
PERCENTAGE = 0.1
DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

generator = SyntheticDataGenerator() # creates the synthetic data generator
dataset = DatasetBuilder() # creates the dataset builder

# Training data ml model
X = []
y = []

for user_id in range(1, USERS + 1): # loop over users

    habit_name, duration_goal = generator.create_habit() # generates a habit + duration goal

    habit = Habit(
        habit_name, 
        duration_goal
        ) # creates a Habit object
    
    dataset.add_user(
        user_id, 
        habit_name,
        duration_goal
        ) # stores the user

    planned_duration = duration_goal

    first_week = True

    last_week_readiness = None
    two_weeks_ago_readiness = None

    for week in range(1, WEEKS + 1): # loop over weeks

        completed_days = 0

        # Checks if there are already two previous weeks for the ML model
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

        for day in DAYS: # loop over days

            actual_duration = generator.generate_actual_duration(planned_duration) # generates actual duration

            completion = int(actual_duration >= planned_duration)

            completed_days += completion

            attempt = DailyAttempt(
                day, 
                planned_duration, 
                actual_duration
            ) # creates DailyAttempt

            habit.add_attempt(attempt) # add the attempt to Habit

            dataset.add_attempt(
                user_id, 
                week, 
                day, 
                planned_duration, 
                actual_duration, 
                completion
            ) # store the attempt in DatasetBuilder

        weekly_completion_rate = completed_days / len(DAYS)

        weekly_readiness = habit.calculate_weekly_readiness()

        if use_for_ml:
            y.append(weekly_completion_rate)

        # Update next weeks planned duration
        if first_week:
            planned_duration = weekly_readiness * duration_goal
            first_week = False
                
        elif weekly_readiness < last_week_readiness: # comparing to the week before
            planned_duration -= PERCENTAGE * duration_goal
            planned_duration = max(planned_duration, 0)

        else:
            planned_duration += PERCENTAGE * duration_goal
            planned_duration = min(planned_duration, duration_goal)

        planned_duration = round(planned_duration)    

        # Move readiness history forward
        two_weeks_ago_readiness = last_week_readiness
        last_week_readiness = weekly_readiness         

dataset.save_to_csv() # after all users are done

# After all the synthetic data was created
predictor = CompletionPredictor()

predictor.train(X, y)
predictions = predictor.predict(X)


print(predictions[:10])
print(y[:10])