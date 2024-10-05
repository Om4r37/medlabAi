import os, warnings, joblib, pickle, pandas as pd, numpy as np
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    accuracy_score,
    roc_auc_score,
)
from sklearn.model_selection import (
    train_test_split,
    cross_val_score,
    RepeatedStratifiedKFold,
)
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MinMaxScaler, StandardScaler, LabelEncoder

warnings.filterwarnings("ignore")
model_path = os.path.join(os.path.dirname(__file__), "models", "heart_attack.pkl")
transformer_path = os.path.join(
    os.path.dirname(__file__), "models", "ha_transformers.pkl"
)


def init():
    print("Initializing heart attack model")
    le = LabelEncoder()
    mms = MinMaxScaler()  # Normalization
    ss = StandardScaler()  # Standardization

    file_path = os.path.join(os.path.dirname(__file__), "data", "heart_attack.csv")
    df = pd.read_csv(file_path)
    # csv header: Age,Sex,ChestPainType,RestingBP,Cholesterol,FastingBS,RestingECG,MaxHR,ExerciseAngina,Oldpeak,ST_Slope,HeartDisease
    # Fit transformers on all data
    le_sex = LabelEncoder().fit(df["Sex"])
    le_chest = LabelEncoder().fit(df["ChestPainType"])
    le_ecg = LabelEncoder().fit(df["RestingECG"])
    le_angina = LabelEncoder().fit(df["ExerciseAngina"])
    le_slope = LabelEncoder().fit(df["ST_Slope"])

    ss_age = StandardScaler().fit(df[["Age"]])
    ss_bp = StandardScaler().fit(df[["RestingBP"]])
    ss_chol = StandardScaler().fit(df[["Cholesterol"]])
    ss_hr = StandardScaler().fit(df[["MaxHR"]])

    mms_peak = MinMaxScaler().fit(df[["Oldpeak"]])

    # Transform data
    df["Sex"] = le_sex.transform(df["Sex"])
    df["ChestPainType"] = le_chest.transform(df["ChestPainType"])
    df["RestingECG"] = le_ecg.transform(df["RestingECG"])
    df["ExerciseAngina"] = le_angina.transform(df["ExerciseAngina"])
    df["ST_Slope"] = le_slope.transform(df["ST_Slope"])

    df["Age"] = ss_age.transform(df[["Age"]])
    df["RestingBP"] = ss_bp.transform(df[["RestingBP"]])
    df["Cholesterol"] = ss_chol.transform(df[["Cholesterol"]])
    df["MaxHR"] = ss_hr.transform(df[["MaxHR"]])

    df["Oldpeak"] = mms_peak.transform(df[["Oldpeak"]])

    features = df[df.columns.drop(["HeartDisease", "RestingBP", "RestingECG"])].values
    target = df["HeartDisease"].values
    x_train, x_test, y_train, y_test = train_test_split(
        features, target, test_size=0.20, random_state=2
    )

    # Save the fitted transformers
    transformers = {
        "le_sex": le_sex,
        "le_chest": le_chest,
        "le_ecg": le_ecg,
        "le_angina": le_angina,
        "le_slope": le_slope,
        "ss_age": ss_age,
        "ss_bp": ss_bp,
        "ss_chol": ss_chol,
        "ss_hr": ss_hr,
        "mms_peak": mms_peak,
    }

    with open(transformer_path, "wb") as f:
        pickle.dump(transformers, f)

    def model(classifier):

        classifier.fit(x_train, y_train)
        # current score is 91.1%
        # prediction = classifier.predict(x_test)
        # cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
        # print("Accuracy : ", "{0:.2%}".format(accuracy_score(y_test, prediction)))
        # print(
        #     "Cross Validation Score : ",
        #     "{0:.2%}".format(
        #         cross_val_score(
        #             classifier, x_train, y_train, cv=cv, scoring="roc_auc"
        #         ).mean()
        #     ),
        # )
        # print("ROC_AUC Score : ", "{0:.2%}".format(roc_auc_score(y_test, prediction)))

    def model_evaluation(classifier):

        # Confusion Matrix
        cm = confusion_matrix(y_test, classifier.predict(x_test))
        names = ["True Neg", "False Pos", "False Neg", "True Pos"]
        counts = [value for value in cm.flatten()]
        percentages = ["{0:.2%}".format(value) for value in cm.flatten() / np.sum(cm)]
        labels = [f"{v1}\n{v2}\n{v3}" for v1, v2, v3 in zip(names, counts, percentages)]
        labels = np.asarray(labels).reshape(2, 2)

        # Classification Report
        print(classification_report(y_test, classifier.predict(x_test)))

    classifier_lr = LogisticRegression(random_state=0, C=10, penalty="l2")
    model(classifier_lr)

    # store the model
    open(model_path, "w").close()
    joblib.dump(classifier_lr, model_path)


def predict(data):
    model = joblib.load(model_path)

    # Load transformers
    with open(transformer_path, "rb") as f:
        transformers = pickle.load(f)

    # Convert data to numpy array if it's not already
    data = np.array(data).reshape(1, -1)

    # Create a DataFrame with column names to match the training data
    columns = [
        "Age",
        "Sex",
        "ChestPainType",
        "RestingBP",
        "Cholesterol",
        "FastingBS",
        "RestingECG",
        "MaxHR",
        "ExerciseAngina",
        "Oldpeak",
        "ST_Slope",
    ]
    df = pd.DataFrame(data, columns=columns)

    # Apply transformations
    df["Age"] = transformers["ss_age"].transform(df[["Age"]])
    df["Sex"] = transformers["le_sex"].transform(df["Sex"])
    df["ChestPainType"] = transformers["le_chest"].transform(df["ChestPainType"])
    df["Cholesterol"] = transformers["ss_chol"].transform(df[["Cholesterol"]])
    df["FastingBS"] = df["FastingBS"]  # Assuming this is already binary
    df["MaxHR"] = transformers["ss_hr"].transform(df[["MaxHR"]])
    df["ExerciseAngina"] = transformers["le_angina"].transform(df["ExerciseAngina"])
    df["Oldpeak"] = transformers["mms_peak"].transform(df[["Oldpeak"]])
    df["ST_Slope"] = transformers["le_slope"].transform(df["ST_Slope"])

    # Drop the columns that were excluded in the training
    df = df.drop(["RestingBP", "RestingECG"], axis=1)

    # Ensure the column order matches the training data
    feature_order = [
        "Age",
        "Sex",
        "ChestPainType",
        "Cholesterol",
        "FastingBS",
        "MaxHR",
        "ExerciseAngina",
        "Oldpeak",
        "ST_Slope",
    ]
    df = df[feature_order]

    # Make prediction
    prediction = model.predict(df)[0]
    # probability = model.predict_proba(df)[0][1]

    return prediction  # , probability


# Example usage:
# print(f"Prediction: {predict([40,'M','ATA',140,289,0,'Normal',172,'N',0,'Up'])}")

try:
    joblib.load(model_path)
except FileNotFoundError:
    init()
