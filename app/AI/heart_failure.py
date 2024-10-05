import os, pandas as pd, joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score

model_path = os.path.join(os.path.dirname(__file__), "models", "heart_failure.pkl")


def init():
    print("Initializing heart failure model")
    file_path = os.path.join(os.path.dirname(__file__), "data", "heart_failure.csv")
    heart_data = pd.read_csv(file_path)

    Features = [
        "age",
        "anaemia",
        "creatinine_phosphokinase",
        "diabetes",
        "ejection_fraction",
        "high_blood_pressure",
        "platelets",
        "serum_creatinine",
        "serum_sodium",
        "sex",
        "smoking",
        "time",
    ]
    x = heart_data[Features]
    y = heart_data["DEATH_EVENT"]
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=2
    )
    accuracy_list = []

    # GradientBoostingClassifier
    gradientboost_clf = GradientBoostingClassifier(max_depth=2, random_state=1)
    gradientboost_clf.fit(x_train, y_train)
    # gradientboost_pred = gradientboost_clf.predict(x_test)
    # gradientboost_acc = accuracy_score(y_test, gradientboost_pred)
    # accuracy_list.append(100 * gradientboost_acc)
    # print(
    #     "Accuracy of Gradient Boosting is : ",
    #     "{:.2f}%".format(100 * gradientboost_acc),
    # )

    # store the model
    joblib.dump(gradientboost_clf, model_path)


def predict(data):
    model = joblib.load(model_path)
    return model.predict([data])[0]


try:
    joblib.load(model_path)
except:
    init()
