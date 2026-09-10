import pandas as pd

class DatasetBuilder:

    def __init__(self): # creates storage for user records and attempts records
        self.user_records = []
        self.attempts_records = []
    
    def add_user(self, user_id, habit_name, duration_goal): # stores ibe user's habit and duration goal
        self.user_records.append({
            "user_id": user_id, 
            "habit_name": habit_name,
            "duration_goal": duration_goal
        })

    def add_attempt(self, user_id, week, day, planned_duration, actual_duration, completion): # stores one daily-attempt record
        self.attempts_records.append({
            "user_id": user_id,
            "week": week,
            "day": day,
            "planned_duration": planned_duration,
            "actual_duration": actual_duration,
            "completion": completion
        })

    def get_users_dataframe(self):
        return pd.DataFrame(self.user_records) # converts user records into a pandas DataFrame
        

    def get_attempts_dataframe(self):
        return pd.DataFrame(self.attempts_records) # converts attempts records into a pandas DataFrame

    def save_to_csv(self):
        # Saves the generated datasets as CSV files
        users_df = self.get_users_dataframe()
        attempts_df = self.get_attempts_dataframe()

        users_df.to_csv("user_records.csv", index=False)
        attempts_df.to_csv("attempts_records.csv", index=False)