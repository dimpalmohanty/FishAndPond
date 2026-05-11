def analyze_pond(sensor):

    issues = []
    recommendations = []

    if sensor["dissolved_oxygen"] < 5:
        issues.append("Low dissolved oxygen")
        recommendations.append("Increase aeration immediately")

    if sensor["ammonia_ppm"] > 0.5:
        issues.append("High ammonia")
        recommendations.append("Reduce feeding and change water")

    if sensor["ph"] < 6.5 or sensor["ph"] > 8.5:
        issues.append("Unsafe pH")
        recommendations.append("Adjust water chemistry gradually")

    # Determine severity
    if len(issues) == 0:
        risk = "SAFE"
    elif len(issues) <= 2:
        risk = "CAUTION"
    else:
        risk = "RISK"

    return {
        "risk_level": risk,
        "issues": issues,
        "recommendations": recommendations
    }