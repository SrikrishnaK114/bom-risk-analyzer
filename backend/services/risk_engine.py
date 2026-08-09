import joblib
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "training" / "risk_model.pkl"

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Risk model not found:\n{MODEL_PATH}"
    )

model = joblib.load(MODEL_PATH)


def parse_voltage(value):
    try:
        return float(
            str(value)
            .replace("V", "")
            .strip()
        )
    except (ValueError, TypeError):
        return 0.0


def parse_current(value):
    try:
        value = str(value).strip().upper()

        if value.endswith("MA"):
            return float(
                value.replace("MA", "")
            ) / 1000

        if value.endswith("A"):
            return float(
                value.replace("A", "")
            )

        return float(value)

    except (ValueError, TypeError):
        return 0.0


def get_risk_level(score):

    if score >= 70:
        return "High"

    elif score >= 40:
        return "Medium"

    return "Low"

def calculate_component_risk(component):

    specs = component.get(
        "electrical_specs",
        {}
    )

    voltage = parse_voltage(
        specs.get("voltage", "0V")
    )

    current = parse_current(
        specs.get("current", "0mA")
    )

    features = pd.DataFrame([{
        "category": component.get(
            "category", ""
        ),

        "package": component.get(
            "package", ""
        ),

        "voltage": voltage,

        "current": current,

        "criticality": component.get(
            "criticality", "Low"
        ),

        "second_source": component.get(
            "second_source", True
        ),

        "lifecycle": component.get(
            "lifecycle", "Active"
        ),

        "lead_time_weeks": component.get(
            "lead_time", 0
        ),

        "availability": component.get(
            "availability", 0
        )
    }])

    try:

        predicted_score = model.predict(
            features
        )[0]

        risk_score = round(
            float(predicted_score)
        )

    except Exception as e:

        print(
            "ML Prediction Error:",
            e
        )

        # Safe fallback
        risk_score = 50


    # Keep score inside 0-100
    risk_score = max(
        0,
        min(100, risk_score)
    )

    risk_level = get_risk_level(
        risk_score
    )

    breakdown = {
        "obsolescence": 0,
        "supply": 0,
        "single_source": 0,
        "criticality": 0
    }

    lifecycle = str(
        component.get(
            "lifecycle",
            ""
        )
    ).upper()

    if lifecycle == "EOL":

        breakdown["obsolescence"] = 60

    elif lifecycle == "NRND":

        breakdown["obsolescence"] = 35

    elif lifecycle == "ACTIVE":

        breakdown["obsolescence"] = 5

    lead_time = float(
        component.get(
            "lead_time",
            0
        )
    )

    availability = float(
        component.get(
            "availability",
            0
        )
    )


    if lead_time > 20:

        breakdown["supply"] += 20

    elif lead_time > 12:

        breakdown["supply"] += 10


    if availability < 5000:

        breakdown["supply"] += 20

    elif availability < 15000:

        breakdown["supply"] += 10

    if component.get(
        "second_source"
    ) is False:

        breakdown["single_source"] = 10

    criticality = str(
        component.get(
            "criticality",
            ""
        )
    ).strip().lower()


    if criticality == "high":

        breakdown["criticality"] = 15

    elif criticality == "medium":

        breakdown["criticality"] = 8

    print("\nDEBUG COMPONENT:")
    print(component)

    print("\nDEBUG ML SCORE:")
    print(risk_score)

    print("\nDEBUG RISK LEVEL:")
    print(risk_level)

    print("\nDEBUG BREAKDOWN:")
    print(breakdown)

    return {
        "part_number": component.get(
            "part_number",
            "Unknown"
        ),

        "risk_score": risk_score,

        "risk_level": risk_level,

        "risk_breakdown": breakdown
    }