
from simulation import SyntheticDataGenerator
from dataset_builder import DatasetBuilder
from habit import DailyAttempt, Habit

USERS = 10 
WEEKS = 10 
PRECENTAGE = 0.1
DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

generator = SyntheticDataGenerator() # creates the synthetic data generator

dataset = DatasetBuilder() # creates the dataset builder

for i in range(1, USERS+1): # loop over users
    user_id = i
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
    previous_readiness = None

    for week in range(1, WEEKS+1): # loop over weeks

        for day in DAYS: # loop over days

            actual_duration = generator.generate_actual_duration(planned_duration) # generates actual duration
            attempt = DailyAttempt(day, planned_duration, actual_duration) # creates DailyAttempt

            habit.add_attempt(attempt) # add the attempt to Habit
            dataset.add_attempt(user_id, week, day, planned_duration, actual_duration) # store the attempt in DatasetBuilder

        weekly_readiness = habit.calculate_weekly_readiness()
        # Update next weeks planned duration
        if first_week:
            planned_duration = weekly_readiness * duration_goal
            first_week = False
                
        elif weekly_readiness < previous_readiness: # comparing to the week before
            planned_duration -= PRECENTAGE * duration_goal
            planned_duration = max(planned_duration, 0)
        else:
            planned_duration += PRECENTAGE * duration_goal
            planned_duration = min (planned_duration, duration_goal)

        planned_duration = round(planned_duration)            
        previous_readiness = weekly_readiness

dataset.save_to_csv() # after all users are done








