from flask import Flask,render_template,request,redirect
from database import db
from models import MachineField, Machine,Prediction
from ml.predictor import predict_risk

app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///machine.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

@app.route("/fields")
def fields():

    all_fields = MachineField.query.all()

    return render_template(
        "fields.html",
        fields=all_fields
    )
@app.route("/")
def home():
    return render_template("index.html")

# def create_default_fields():
#     if MachineField.query.count() == 0:

#         fields = [
#             MachineField(
#                 field_name="Machine Name",
#                 field_type="text",
#                 required=True
#             ),
#             MachineField(
#                 field_name="Temperature",
#                 field_type="number",
#                 required=True
#             ),

#             MachineField(
#                 field_name="Pressure",
#                 field_type="number",
#                 required=True
#             ),

#             MachineField(
#                 field_name="Vibration",
#                 field_type="dropdown",
#                 required=True,
#                 options="Low,Medium,High"
#             )
#         ]
#         db.session.add_all(fields)
#         db.session.commit()

@app.route("/fields/add", methods=["GET", "POST"])
def add_field():

    if request.method == "POST":

        field_name = request.form["field_name"]
        field_type = request.form["field_type"]

        required = "required" in request.form

        options = request.form.get("options")

        new_field = MachineField(
            field_name=field_name,
            field_type=field_type,
            required=required,
            options=options
        )

        db.session.add(new_field)
        db.session.commit()

        return redirect("/fields")

    return render_template("add_field.html")

@app.route("/machines")
def machines():

    all_machines = Machine.query.all()

    return render_template(
        "machines.html",
        machines=all_machines
    )
@app.route("/machines/add", methods=["GET", "POST"])
def add_machine():

    all_fields = MachineField.query.all()

    if request.method == "POST":

        machine_data = {}

        for field in all_fields:

            value = request.form.get(field.field_name)

            if field.field_type == "number":
                value = float(value)

            machine_data[field.field_name] = value

        new_machine = Machine(
            data=machine_data
        )

        db.session.add(new_machine)
        db.session.commit()

        return redirect("/machines")

    return render_template(
        "machine_form.html",
        fields=all_fields
    )


@app.route("/machines/edit/<int:id>", methods=["GET", "POST"])
def edit_machine(id):

    machine = Machine.query.get_or_404(id)

    all_fields = MachineField.query.all()

    if request.method == "POST":

        machine_data = {}

        for field in all_fields:

            value = request.form.get(field.field_name)

            if field.field_type == "number":
                value = float(value)

            machine_data[field.field_name] = value

        machine.data = machine_data

        db.session.commit()

        return redirect("/machines")

    return render_template(
        "edit_machine.html",
        machine=machine,
        fields=all_fields
    )

@app.route("/machines/delete/<int:id>")
def delete_machine(id):

    machine = Machine.query.get_or_404(id)

    db.session.delete(machine)

    db.session.commit()

    return redirect("/machines")

# @app.route("/machines/predict/<int:id>")
# def predict_machine_risk(id):

#     machine = Machine.query.get_or_404(id)

#     temperature = machine.data.get("Temperature")
#     pressure = machine.data.get("Pressure")
#     vibration = machine.data.get("Vibration")

#     risk = predict_risk(
#         temperature,
#         pressure,
#         vibration
#     )

#     return render_template(
#         "risk_result.html",
#         machine=machine,
#         risk=risk
#     )

@app.route("/machines/predict/<int:id>")
def predict_machine_risk(id):

    machine = Machine.query.get_or_404(id)

    temperature = machine.data.get("Temperature")
    pressure = machine.data.get("Pressure")
    vibration = machine.data.get("Vibration")

    if temperature is None:
        return render_template(
            "risk_result.html",
            machine=machine,
            error="Temperature is missing."
        )

    if pressure is None:
        return render_template(
            "risk_result.html",
            machine=machine,
            error="Pressure is missing."
        )

    if vibration is None:
        return render_template(
            "risk_result.html",
            machine=machine,
            error="Vibration is missing."
        )

    try:
        temperature = float(temperature)
        pressure = float(pressure)

    except ValueError:
        return render_template(
            "risk_result.html",
            machine=machine,
            error="Temperature and Pressure must be numbers."
        )

    risk = predict_risk(
        temperature,
        pressure,
        vibration
    )
    prediction = Prediction(
    machine_id=machine.id,
    temperature=temperature,
    pressure=pressure,
    vibration=vibration,
    risk=risk
    )

    db.session.add(prediction)
    db.session.commit()

    return render_template(
        "risk_result.html",
        machine=machine,
        risk=risk
    )

@app.route("/predictions")
def predictions():

    all_predictions = Prediction.query.order_by(
        Prediction.created_at.desc()
    ).all()

    return render_template(
        "predictions.html",
        predictions=all_predictions
    )

@app.route("/dashboard")
def dashboard():

    total_machines = Machine.query.count()

    low_risk = Prediction.query.filter_by(
        risk="Low"
    ).count()

    medium_risk = Prediction.query.filter_by(
        risk="Medium"
    ).count()

    high_risk = Prediction.query.filter_by(
        risk="High"
    ).count()

    recent_predictions = Prediction.query.order_by(
        Prediction.created_at.desc()
    ).limit(10).all()

    return render_template(
        "dashboard.html",
        total_machines=total_machines,
        low_risk=low_risk,
        medium_risk=medium_risk,
        high_risk=high_risk,
        recent_predictions=recent_predictions
    )


# @app.route("/fields/delete/<int:field_id>")
# def delete_field(field_id):
#     field = MachineField.query.get_or_404(field_id)

#     db.session.delete(field)
#     db.session.commit()

#     return redirect("/fields")


if __name__=="__main__":
    with app.app_context():
        db.create_all()

app.run(debug=True)



