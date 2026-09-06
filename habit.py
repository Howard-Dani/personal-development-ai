

class DailyAttempt:

    def __init__(self, day, planned_duration, actual_duration):
        # Stores one day's day, planned_duration and actual_duration
        self.day = day
        self.planned_duration = planned_duration
        self.actual_duration = actual_duration

    def calculate_daily_readiness(self):
        if self.planned_duration == 0:
            return 0
                
        return self.actual_duration / self.planned_duration
    

class Habit:

    def __init__(self, habit_name, duration_goal):
        # Stores habit_name, duration_goal, and the list of attempts
        self.habit_name = habit_name
        self.duration_goal = duration_goal
        self.attempts = []

    def add_attempt(self, attempt):
        self.attempts.append(attempt) # add a DailyAttempt object to the habit


    def calculate_weekly_readiness(self):
        latest_attempts = self.attempts[-7:] # calculate the average readiness of the latest 7 ettempts

        if len(latest_attempts) == 0:
            return 0

        total_readiness = 0
        for attempt in latest_attempts:
            total_readiness += attempt.calculate_daily_readiness()
        return total_readiness / len(latest_attempts)

