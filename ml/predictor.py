import joblib

model = joblib.load(
    "ml/risk_model.pkl"
)

vibration_encoder = joblib.load(
    "ml/vibration_encoder.pkl"
)

def predict_risk(temperature, pressure, vibration):

    vibration_encoded = vibration_encoder.transform(
        [vibration]
    )[0]

    machine_data = [[
        temperature,
        pressure,
        vibration_encoded
    ]]

    prediction = model.predict(
        machine_data
    )

    return prediction[0]
