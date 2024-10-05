import pandas as pd, joblib, warnings, os
from sklearn.discriminant_analysis import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE

warnings.filterwarnings("ignore")
model_path = os.path.join(os.path.dirname(__file__), "models", "diabetes_model.pkl")


def init():
    print("Initializing diabetes model")
    try:
        file_path = os.path.join(os.path.dirname(__file__), "data", "diabetes.csv")
        df = pd.read_csv(file_path)

        def remove_outliers(df, col):
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            return df[(df[col] > lower_bound) & (df[col] < upper_bound)]

        # fill missing values
        for i in ("Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"):
            df[i] = df[i].replace(0, df[i].mean())

        # remove outliers
        for col in df.columns:
            if col != "Outcome":
                df = remove_outliers(df, col)

        X = df[
            [
                "Pregnancies",
                "Glucose",
                "BloodPressure",
                "SkinThickness",
                "Insulin",
                "BMI",
                "DiabetesPedigreeFunction",
                "Age",
            ]
        ]
        y = df["Outcome"]
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

        # cross validation score (current score is 88.4%)
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
    
    except Exception as e:
        print("The error is: ",e)


def predict(data):
    model = joblib.load(model_path)
    return model.predict([data])[0]


if not os.path.exists(model_path):
    init()

try:
    joblib.load(model_path)

# make sure to raise error msg to user if this exception happened 
# and redirect it to same page again 
except Exception as e:
    print("The error is: ",e)
