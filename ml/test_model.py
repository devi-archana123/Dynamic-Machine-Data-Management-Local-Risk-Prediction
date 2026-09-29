import joblib

model = joblib.load(
    "ml/risk_model.pkl"
)

vibration_encoder = joblib.load(
    "ml/vibration_encoder.pkl"
)
# temperature = 50
# pressure = 100
# vibration = "Low"


temperature = 65
pressure = 115
vibration = "Medium"

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

print("Predicted Risk:", prediction[0])
