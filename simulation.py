import random

class SyntheticDataGenerator:


    def create_habit(self):
        habits = [
            'Running', 
            'Studying', 
            'Reading'
            ] # randomly creates a habit name and duration goal

        habit_name = random.choice(habits)
        duration_goal = random.randint(20,120)

        return habit_name, duration_goal


    def create_base_readiness(self):
        base_readiness = random.uniform(0.4, 0.9) # variation base

        return base_readiness


    def create_weekly_condition(self):
        weekly_condition = random.uniform(-0.1, 0.1) # simulates a good or a bad week

        return weekly_condition


    def calculate_completion_probability(
            self,
            planned_duration,
            duration_goal,
            base_readiness,
            weekly_condition,
            previous_planned_duration
    ):

        difficulty = planned_duration / duration_goal # how difficult is the current plan compared with the final goal?

        difficulty  = min(max(difficulty, 0), 1)

        difficulty_bonus = 0.35 * (1 - difficulty) # easier plans get higher probability of completion


        # Penalty if the planned duration increased too quickly
        progression_penalty = 0

        if(
            previous_planned_duration is not None
            and previous_planned_duration > 0
        ):

            progression_change = (planned_duration - previous_planned_duration
                                  ) / previous_planned_duration

            if progression_change > 0.05:

                progression_penalty = (
                    progression_change - 0.05
                ) * 0.8


        completion_probability=(
            base_readiness 
            + difficulty_bonus
            + weekly_condition
            - progression_penalty
        ) # combine all the factors


        completion_probability = min(max(completion_probability, 0.05),
                                     0.95) # upper and lower bound

        return completion_probability


    def generate_actual_duration(
                                self, 
                                 planned_duration,
                                 duration_goal,
                                 base_readiness,
                                 weekly_condition,
                                 previous_planned_duration
                                 ):


        completion_probability = (self.calculate_completion_probability(
            planned_duration,
            duration_goal,
            base_readiness,
            weekly_condition,
            previous_planned_duration
            )
        )


        completed =random.random() < completion_probability

        if completed:
            actual_duration = random.uniform(planned_duration, planned_duration * 1.1)

        else:
            actual_duration = random.uniform(planned_duration * 0.4, planned_duration * 0.95)


        return round(actual_duration)
 