
from sklearn.gaussian_process import GaussianProcessRegressor


class SurrogateModel(object):

    def __init__(self):
        self.x_train = None
        self.y_train = None
        self.gp = None

    def fit(self, X, y):
        self.x_train = X
        self.y_train = y
        self.gp = GaussianProcessRegressor().fit(X, y)

    def predict(self, X):
        y = self.gp.predict(X)
        return y

    def save(self, location):
        pass

    def load(self, location):
        pass