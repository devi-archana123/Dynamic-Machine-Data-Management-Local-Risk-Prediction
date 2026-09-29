from database import db
from datetime import datetime

class MachineField(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    field_name=db.Column(db.String(100),nullable=False)
    field_type=db.Column(db.String(20),nullable=False)
    required=db.Column(db.Boolean,default=False)
    options=db.Column(db.Text,nullable=True)

class Machine(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    data=db.Column(db.JSON,nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Prediction(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    machine_id = db.Column(
        db.Integer,
        nullable=False
    )

    temperature = db.Column(
        db.Float,
        nullable=False
    )

    pressure = db.Column(
        db.Float,
        nullable=False
    )

    vibration = db.Column(
        db.String(50),
        nullable=False
    )

    risk = db.Column(
        db.String(20),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
