import pandas as pd
import joblib

from pathlib import Path

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

# Locate the dataset
base_dir = Path(__file__).parent
dataset_path = base_dir / "component_dataset.csv"

# Read dataset
df = pd.read_csv(dataset_path)

print(df.head())
print("\nDataset Shape:", df.shape)

# Target column
target = "overall_risk"

# Features used for prediction
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

X = df[feature_columns]
y = df[target]

print("\nFeatures:")
print(X.head())

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print(f"\nTraining samples: {len(X_train)}")
print(f"Testing samples: {len(X_test)}")

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
            "cat",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        )
    ],
    remainder="passthrough"
)

model = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(
        n_estimators=200,
        random_state=42
    ))
])

print("\nTraining model...")

model.fit(X_train, y_train)

print("Training complete!")

predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)

print(f"\nMean Absolute Error: {mae:.2f}")

model_path = base_dir / "risk_model.pkl"

joblib.dump(model, model_path)

print("\nModel saved successfully!")
print(f"Location: {model_path}")