from sklearn.ensemble import RandomForestRegressor

# What is the probability that this user will  complete a proposed duration?

class CompletionPredictor:
    def __init__(self):
        self.model = RandomForestRegressor()

    def train(self, X, y):
        self.model.fit(X,y)

    def predict(self, X):
        return self.model.predict(X)
    


