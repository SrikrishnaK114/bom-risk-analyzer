import joblib
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "training" / "risk_model.pkl"

model = joblib.load(MODEL_PATH)

def parse_voltage(value):
    
    try:
        return float(str(value).replace("V", "").strip())
    except:
        return 0.0


def parse_current(value):
    
    try:
        value = str(value).strip().upper()

        if value.endswith("MA"):
            return float(value.replace("MA", "")) / 1000

        elif value.endswith("A"):
            return float(value.replace("A", ""))

        return float(value)

    except:
        return 0.0


def calculate_component_risk(component):
   
    specs = component.get("electrical_specs", {})

    voltage = parse_voltage(specs.get("voltage", "0V"))
    current = parse_current(specs.get("current", "0mA"))

    features = pd.DataFrame([{
        "category": component.get("category", ""),
        "package": component.get("package", ""),
        "voltage": voltage,
        "current": current,
        "criticality": component.get("criticality", "Low"),
        "second_source": component.get("second_source", True),
        "lifecycle": component.get("lifecycle", "Active"),
        "lead_time_weeks": component.get("lead_time", 0),
        "availability": component.get("availability", 0)
    }])

    try:
        risk_score = round(float(model.predict(features)[0]))

    except Exception as e:
        print("Prediction Error:", e)
        risk_score = 50

    if risk_score >= 70:
        risk_level = "High"

    elif risk_score >= 40:
        risk_level = "Medium"

    else:
        risk_level = "Low"

    breakdown = {
        "obsolescence": 0,
        "supply": 0,
        "single_source": 0,
        "criticality": 0
    }

    lifecycle = component.get("lifecycle", "").upper()

    if lifecycle == "EOL":
        breakdown["obsolescence"] = 50

    elif lifecycle == "NRND":
        breakdown["obsolescence"] = 30

    lead_time = component.get("lead_time", 0)
    availability = component.get("availability", 0)

    if lead_time > 16:
        breakdown["supply"] += 15

    if availability < 5000:
        breakdown["supply"] += 15

    if component.get("second_source") is False:
        breakdown["single_source"] = 10

    criticality = component.get("criticality", "").lower()

    if criticality == "high":
        breakdown["criticality"] = 15

    elif criticality == "medium":
        breakdown["criticality"] = 8

    return {
        "part_number": component.get("part_number", "Unknown"),
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_breakdown": breakdown
    }