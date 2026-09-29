import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

import joblib

# 1. Load the dataset
data = pd.read_csv("ml/machine_data.csv")

print("Dataset:")
print(data)

print("\nDataset shape:")
print(data.shape)

# 2. Convert vibration to numbers
vibration_encoder = LabelEncoder()

data["vibration"] = vibration_encoder.fit_transform(
    data["vibration"]
)

# 3. Separate input and output
X = data[
    [
        "temperature",
        "pressure",
        "vibration"
    ]
]

y = data["risk"]

# 4. Split the dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# 5. Create the ML model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# 6. Train the model
model.fit(X_train, y_train)

# 7. Test the model
predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print("\nModel Accuracy:")
print(accuracy)

# 8. Save the model
joblib.dump(
    model,
    "ml/risk_model.pkl"
)

joblib.dump(
    vibration_encoder,
    "ml/vibration_encoder.pkl"
)

print("\nModel saved successfully!")
