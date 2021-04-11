from sklearn.linear_model import LogisticRegression
from sklearn2pmml.pipeline import PMMLPipeline
from sklearn2pmml import sklearn2pmml

import numpy as np
import pandas as pd
import joblib


class LogisticRegressionClassifier:
    def __init__(self, penalty='l2', max_iter=500, solver='lbfgs'):
        self.clf = LogisticRegression(penalty=penalty, max_iter=max_iter, solver=solver, multi_class='multinomial')

    def fit(self, x_train, y_train):
        self.clf.fit(x_train, y_train)

    def predict(self, x_test):
        predictions = self.clf.predict(x_test)
        return predictions

    def score(self, x_test, y_test):
        predictions = self.predict(x_test)
        return (predictions == y_test).sum().astype(np.float64) / len(y_test)

    def export(self, file_name):
        joblib.dump(self.clf, file_name)


df = pd.read_csv('../data/combined_data.csv')
# Get dictionary for categorical coding
c = df.Label.astype('category')
code_to_posture = dict(enumerate(c.cat.categories))
print(code_to_posture)
# Categorical coding
df['Label'] = df['Label'].astype('category').cat.codes

# Subtract baseline from each reading
# baselines = list(df['Baseline'].values)
# for i, baseline in enumerate(baselines):
#     temp = baseline.split(",")
#     for j, x in enumerate(temp):
#         temp[j] = int(float(x))
#     baselines[i] = temp
# baselines = np.array(baselines)
# for i in range(8):
#     df.iloc[:, [i]] = df.iloc[:, [i]] - baselines[:, i].reshape(len(baselines[:, i]), 1)

# Shuffle and divide feature and label
np.random.seed(4321)
df_shuffle = df.sample(frac=1).drop(['Baseline'], axis=1)
df_x = df_shuffle.drop(['Label'], axis=1).values
df_y = df_shuffle['Label'].values

# Standardizing predictors to zero mean unit variance
df_x = (df_x - df_x.mean()) / df_x.std()

# Separate training, validation, and testing data
x_train, x_test = np.split(df_x, [int(0.8 * len(df_x))])
y_train, y_test = np.split(df_y, [int(0.8 * len(df_y))])

# PMML Conversion
pipeline = PMMLPipeline([
    ("classifier", LogisticRegression(penalty='l2', max_iter=1000, solver='lbfgs', multi_class='multinomial'))
])
pipeline.fit(df_x, df_y)
sklearn2pmml(pipeline, "lr.pmml")

# clf = LogisticRegressionClassifier()
# clf.fit(x_train, y_train)
# y_predict = clf.predict(x_test)
#
# # Converting coding back to posture
# predicted_postures = []
# for y in y_predict:
#     predicted_postures.append(code_to_posture[y])
# print(predicted_postures)
#
# print(clf.score(x_test, y_test))
# file_name = "logistic_regression_model.pkl"
# clf.export(file_name)

