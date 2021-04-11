import pandas as pd
import numpy as np
from classifier.logistic_regression import LogisticRegressionClassifier
from classifier.random_forest import RandomForest
from classifier.knearestneighbor import KNearestNeighbor


def test_clf(clf, seed):
    df = pd.read_csv('data/combined_data.csv')
    # Get dictionary for categorical coding
    c = df.Label.astype('category')
    code_to_posture = dict(enumerate(c.cat.categories))
    # Categorical coding
    df['Label'] = df['Label'].astype('category').cat.codes

    # Subtract baseline from each reading
    baselines = list(df['Baseline'].values)
    for i, baseline in enumerate(baselines):
        temp = baseline.split(",")
        for j, x in enumerate(temp):
            temp[j] = int(float(x))
        baselines[i] = temp
    baselines = np.array(baselines)
    for i in range(8):
        df.iloc[:, [i]] = df.iloc[:, [i]] - baselines[:, i].reshape(len(baselines[:, i]), 1)

    # Shuffle and divide feature and label
    np.random.seed(seed)
    df_shuffle = df.sample(frac=1).drop(['Baseline'], axis=1)
    df_x = df_shuffle.drop(['Label'], axis=1).values
    df_y = df_shuffle['Label'].values
    # Standardizing predictors to zero mean unit variance
    df_x = (df_x - df_x.mean()) / df_x.std()

    # Separate training, validation, and testing data
    x_train, x_test = np.split(df_x, [int(0.8 * len(df_x))])
    y_train, y_test = np.split(df_y, [int(0.8 * len(df_y))])

    clf.fit(x_train, y_train)
    y_predict = clf.predict(x_test)

    # Converting coding back to posture
    predicted_postures = []
    for y in y_predict:
        predicted_postures.append(code_to_posture[y])

    if isinstance(clf, KNearestNeighbor):
        print(x_test)
        knn_pred = clf.predict_proba(x_test)
        print(knn_pred)
        print(y_test)
        return clf.score(x_test, y_test)
    return clf.score(x_test, y_test)

if __name__ == '__main__':
    knn_clf = KNearestNeighbor()
    rf_clf = RandomForest()
    lr_clf = LogisticRegressionClassifier()

    test_seed = np.random.randint(10000)

    knn_score= test_clf(knn_clf, test_seed)
    rf_score = test_clf(rf_clf, test_seed)
    lr_score = test_clf(lr_clf, test_seed)


    score = [knn_score, rf_score, lr_score]
    print(score)