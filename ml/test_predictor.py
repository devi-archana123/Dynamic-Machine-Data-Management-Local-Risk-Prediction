from predictor import predict_risk


risk = predict_risk(
    85,
    130,
    "High"
)


print("Predicted Risk:", risk)
