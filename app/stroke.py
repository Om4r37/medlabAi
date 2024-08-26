import pandas as pd, numpy as np, joblib, warnings, os
from sklearn.discriminant_analysis import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeRegressor
from imblearn.over_sampling import SMOTE

warnings.filterwarnings("ignore")
model_path = os.path.join(os.path.dirname(__file__), "models", "stroke_model.pkl")


def init():
    print("Initializing stroke model")
    file_path = os.path.join(os.path.dirname(__file__), "data", "stroke.csv")
    df = pd.read_csv(file_path)

    # fill missing values
    DT_bmi_pipe = Pipeline(
        steps=[
            ("scale", StandardScaler()),
            ("lr", DecisionTreeRegressor(random_state=42)),
        ]
    )
    X = df[["age", "gender", "bmi"]].copy()
    X.gender = X.gender.replace({"Male": 0, "Female": 1, "Other": -1}).astype(np.uint8)

    Missing = X[X.bmi.isna()]
    X = X[~X.bmi.isna()]
    Y = X.pop("bmi")
    DT_bmi_pipe.fit(X, Y)
    predicted_bmi = pd.Series(
        DT_bmi_pipe.predict(Missing[["age", "gender"]]), index=Missing.index
    )
    df.loc[Missing.index, "bmi"] = predicted_bmi

    # Encoding categorical values

    df["gender"] = (
        df["gender"].replace({"Male": 1, "Female": 0, "Other": -1}).astype(np.uint8)
    )
    df["Residence_type"] = (
        df["Residence_type"].replace({"Rural": 0, "Urban": 1}).astype(np.uint8)
    )
    df["work_type"] = (
        df["work_type"]
        .replace(
            {
                "Private": 1,
                "Self-employed": 2,
                "Govt_job": 3,
                "children": 4,
                "Never_worked": 0,
            }
        )
        .astype(np.uint8)
    )

    X = df[
        [
            "gender",
            "age",
            "hypertension",
            "heart_disease",
            "work_type",
            "avg_glucose_level",
            "bmi",
        ]
    ]
    y = df["stroke"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, train_size=0.3, random_state=42
    )

    # Our data is biased, we can fix this with SMOTE

    oversample = SMOTE()
    X_train_resh, y_train_resh = oversample.fit_resample(X_train, y_train.ravel())

    # random forest classifier
    rf_pipeline = Pipeline(
        steps=[
            ("scale", StandardScaler()),
            ("RF", RandomForestClassifier(random_state=42)),
        ]
    )

    # train the model
    rf_pipeline.fit(X_train_resh, y_train_resh)

    # cross validation score (current score is 94.2%)
    # rf_cv = cross_val_score(
    #     rf_pipeline, X_train_resh, y_train_resh, cv=10, scoring="f1"
    # )
    # print(
    #     "Random Forest mean :",
    #     cross_val_score(
    #         rf_pipeline, X_train_resh, y_train_resh, cv=10, scoring="f1"
    #     ).mean(),
    # )

    # store the model
    open(model_path, "w").close()
    joblib.dump(rf_pipeline, model_path)


def predict(data):
    model = joblib.load(model_path)
    return model.predict([data])[0]


try:
    joblib.load(model_path)
except FileNotFoundError:
    init()
