import pandas as pd
import random

class SyntheticDataGenerator:

    def create_habit(self):
        habits = [
            'Running', 
            'Studing', 
            'Reading'
            ] # randomly creates a habit name and duration goal
        habit_name = random.choice(habits)
        duration_goal = random.randint(20,120)

        return habit_name, duration_goal
        
    def generate_actual_duration(self, planned_duration):
        lower_bound = round(planned_duration * 0.5)
        upper_bound = round(planned_duration * 1.2)

        actual_duration = random.randint(lower_bound, upper_bound) # generates a synthetic actual duration for one day
        return actual_duration
 