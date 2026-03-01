from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class ShipmentData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shipment_id = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    weight = db.Column(db.Float)
    tamper_status = db.Column(db.Boolean)
    risk_score = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)