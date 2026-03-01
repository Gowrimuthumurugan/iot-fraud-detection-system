def calculate_risk(weight, expected_weight, tamper_status, geo_deviation):
    risk = 0

    # Weight variation logic
    if abs(weight - expected_weight) > 5:
        risk += 30

    # Tamper detection
    if tamper_status:
        risk += 40

    # Geo deviation
    if geo_deviation:
        risk += 30

    return min(risk, 100)