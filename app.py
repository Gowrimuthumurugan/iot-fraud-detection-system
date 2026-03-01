from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from config import Config
from models import db, ShipmentData
from risk_engine import calculate_risk

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
CORS(app)

# Create DB
with app.app_context():
    db.create_all()

EXPECTED_WEIGHT = 100.0
ALLOWED_LAT = 11.0
ALLOWED_LON = 77.0
GEO_RADIUS = 0.5


def check_geo_fence(lat, lon):
    if abs(lat - ALLOWED_LAT) > GEO_RADIUS or abs(lon - ALLOWED_LON) > GEO_RADIUS:
        return True
    return False


# ===============================
# API: Receive IoT Sensor Data
# ===============================
@app.route("/api/sensor-data", methods=["POST"])
def receive_sensor_data():
    data = request.json

    shipment_id = data["shipment_id"]
    latitude = data["latitude"]
    longitude = data["longitude"]
    weight = data["weight"]
    tamper_status = data["tamper_status"]

    geo_deviation = check_geo_fence(latitude, longitude)

    risk_score = calculate_risk(
        weight,
        EXPECTED_WEIGHT,
        tamper_status,
        geo_deviation
    )

    shipment = ShipmentData(
        shipment_id=shipment_id,
        latitude=latitude,
        longitude=longitude,
        weight=weight,
        tamper_status=tamper_status,
        risk_score=risk_score
    )

    db.session.add(shipment)
    db.session.commit()

    return jsonify({
        "message": "Data stored successfully",
        "risk_score": risk_score,
        "geo_deviation": geo_deviation
    })


# ===============================
# API: Get All Shipments
# ===============================
@app.route("/api/shipments", methods=["GET"])
def get_shipments():
    shipments = ShipmentData.query.all()

    result = []
    for s in shipments:
        result.append({
            "shipment_id": s.shipment_id,
            "latitude": s.latitude,
            "longitude": s.longitude,
            "weight": s.weight,
            "tamper_status": s.tamper_status,
            "risk_score": s.risk_score,
            "timestamp": s.timestamp
        })

    return jsonify(result)


# Serve the frontend
@app.route("/")
def serve_index():
    return send_file("index.html")


if __name__ == "__main__":
    app.run(debug=True)
    