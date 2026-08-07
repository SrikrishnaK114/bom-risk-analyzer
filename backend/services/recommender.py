import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = BASE_DIR / "data" / "component_master.csv"

component_db = pd.read_csv(DATASET_PATH)
component_db["second_source"] = component_db["second_source"].astype(str).str.lower()


def find_best_substitute(component):
    """
    Finds the most compatible substitute for a component.

    Input:
        component (dict)

    Output:
        dict
    """
    specs = component.get("electrical_specs", {})

    target_voltage = float(specs.get("voltage", "0V").replace("V", ""))

    target_current = float(specs.get("current", "0mA").replace("mA", "")) / 1000
    best_component = None
    best_score = -1
    uploaded_group = component.get("substitute_group", None)
    if uploaded_group:
        candidates = component_db[
            component_db["substitute_group"] == uploaded_group
        ]
    else:
        candidates = component_db
    for _, candidate in candidates.iterrows():
            if candidate["part_number"] == component["part_number"]:
                continue
            score=0
            reasons=[]
            if candidate["category"] == component["category"]:
                score += 30
                reasons.append("Same category")
            if candidate["package"] == component["package"]:
                score += 30
                reasons.append("Same package")
            else:
                reasons.append("Package mismatch")
            if abs(candidate["voltage"] - target_voltage) <= 0.5:
                score += 20
                reasons.append("Voltage compatible")
            if abs(candidate["current"] - target_current) <= 0.1:
                score += 20
                reasons.append("Current compatible")
            candidate_tolerance = str(candidate["tolerance"])
            target_tolerance = str(specs.get("tolerance", ""))

            if candidate_tolerance == target_tolerance:
                score += 10
                reasons.append("Tolerance compatible")
            if score > best_score:
                best_score = score
                best_component = {
                    "part_number": candidate["part_number"],
                    "score": score,
                    "reason": ", ".join(reasons)
                }

    if best_component is None:
        return None

    if best_score >= 90 and "Package mismatch" not in best_component["reason"]:
        recommendation_type = "Exact Drop-in"

    elif best_score >= 70:
        recommendation_type = "Minor Redesign"

    else:
        recommendation_type = "Requires Redesign"

    return {
        "best_alternative": best_component["part_number"],
        "compatibility_percentage": min(best_score, 100),
        "alternative_type": recommendation_type,
        "reason": best_component["reason"]
    }

if __name__ == "__main__":

    sample_component = {
    "part_number": "STM32F103C8",
    "category": "MCU",
    "package": "LQFP48",
    "criticality": "High",
    "second_source": False,
    "lifecycle": "Active",
    "lead_time": 12,
    "availability": 14500,
    "electrical_specs": {
        "voltage": "3.3V",
        "current": "50mA",
        "tolerance": "±5%"
    }
}

    recommendation = find_best_substitute(sample_component)

    print("\nRecommendation:")
    print(recommendation)
