from sklearn.ensemble import RandomForestRegressor

class CompletionPredictor: # forecast behaviour
    def __init__(self):
        self.model = RandomForestRegressor(random_state=42)

    def train(self, X, y):
        self.model.fit(X,y)

    def predict(self, X):
        return self.model.predict(X)
    
class ProgressionRecommender: # make a decision
    
    def progression_calculation(self, predictions):

        if predictions < 0.5:
            progression = 0.9

        elif predictions < 0.7:
            progression = 1

        elif predictions < 0.85:
            progression = 1.05

        else:
            progression = 1.1


        return progression

