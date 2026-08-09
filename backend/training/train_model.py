import pandas as pd
import joblib

from pathlib import Path

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATASET_PATH = (
    BASE_DIR
    / "component_dataset.csv"
)

MODEL_PATH = (
    BASE_DIR
    / "risk_model.pkl"
)


# ============================================================
# LOAD DATASET
# ============================================================

df = pd.read_csv(
    DATASET_PATH
)

print(
    "Dataset shape:",
    df.shape
)


# ============================================================
# FEATURES
# ============================================================

feature_columns = [

    "category",
    "package",
    "voltage",
    "current",
    "criticality",
    "second_source",
    "lifecycle",
    "lead_time_weeks",
    "availability"

]

target = "overall_risk"


X = df[
    feature_columns
]

y = df[
    target
]


# ============================================================
# TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.2,

    random_state=42
)


print(
    f"Training samples: {len(X_train)}"
)

print(
    f"Testing samples: {len(X_test)}"
)


# ============================================================
# PREPROCESSING
# ============================================================

categorical_features = [

    "category",
    "package",
    "criticality",
    "second_source",
    "lifecycle"

]


numeric_features = [

    "voltage",
    "current",
    "lead_time_weeks",
    "availability"

]


preprocessor = ColumnTransformer(

    transformers=[

        (
            "categorical",

            OneHotEncoder(
                handle_unknown="ignore"
            ),

            categorical_features
        )

    ],

    remainder="passthrough"
)


# ============================================================
# MODEL
# ============================================================

model = Pipeline([

    (
        "preprocessor",
        preprocessor
    ),

    (
        "regressor",

        RandomForestRegressor(

            n_estimators=300,

            random_state=42,

            min_samples_leaf=2
        )
    )

])


# ============================================================
# TRAIN
# ============================================================

print(
    "\nTraining model..."
)


model.fit(
    X_train,
    y_train
)


print(
    "Training complete!"
)


# ============================================================
# EVALUATION
# ============================================================

predictions = model.predict(
    X_test
)


mae = mean_absolute_error(
    y_test,
    predictions
)


print(
    f"\nMean Absolute Error: {mae:.2f}"
)


# ============================================================
# RISK LEVEL
# ============================================================

def risk_level(score):

    if score >= 70:
        return "High"

    elif score >= 40:
        return "Medium"

    return "Low"


actual_levels = y_test.apply(
    risk_level
)


predicted_levels = pd.Series(
    predictions,
    index=y_test.index
).apply(
    risk_level
)


accuracy = (
    actual_levels
    == predicted_levels
).mean()


print(
    f"Risk Level Accuracy: "
    f"{accuracy * 100:.2f}%"
)


# ============================================================
# SAVE MODEL
# ============================================================

joblib.dump(
    model,
    MODEL_PATH
)


print(
    "\nModel saved successfully!"
)

print(
    f"Location: {MODEL_PATH}"
)