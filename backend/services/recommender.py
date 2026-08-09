import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = BASE_DIR / "data" / "component_master.csv"

if not DATASET_PATH.exists():
    raise FileNotFoundError(
        f"Component master file not found:\n{DATASET_PATH}"
    )

component_db = pd.read_csv(DATASET_PATH)

component_db.columns = (
    component_db.columns
    .str.strip()
    .str.lower()
)

component_db["part_number"] = (
    component_db["part_number"]
    .astype(str)
    .str.strip()
)

def find_best_substitute(component):
    
    specs = component.get("electrical_specs", {})

    try:
        target_voltage = float(
            str(specs.get("voltage", "0V"))
            .replace("V", "")
            .strip()
        )
    except (ValueError, TypeError):
        target_voltage = 0.0

    try:
        current_value = (
            str(specs.get("current", "0mA"))
            .strip()
            .upper()
        )

        if current_value.endswith("MA"):
            target_current = (
                float(current_value.replace("MA", ""))
                / 1000
            )
        elif current_value.endswith("A"):
            target_current = float(
                current_value.replace("A", "")
            )
        else:
            target_current = float(current_value)

    except (ValueError, TypeError):
        target_current = 0.0

    target_part = str(
        component.get("part_number", "")
    ).strip()

    target_category = str(
        component.get("category", "")
    ).strip()

    target_package = str(
        component.get("package", "")
    ).strip()

    target_tolerance = str(
        specs.get("tolerance", "")
    ).strip()

    candidates = component_db.copy()

    # Never recommend the component itself
    candidates = candidates[
        candidates["part_number"].str.upper()
        != target_part.upper()
    ]

    # Prefer same category
    same_category = candidates[
        candidates["category"]
        .astype(str)
        .str.strip()
        .str.lower()
        == target_category.lower()
    ]

    if not same_category.empty:
        candidates = same_category

    best_component = None
    best_score = -1

    for _, candidate in candidates.iterrows():

        score = 0
        reasons = []

        candidate_category = str(
            candidate["category"]
        ).strip()

        candidate_package = str(
            candidate["package"]
        ).strip()

        if (
            candidate_category.lower()
            == target_category.lower()
        ):
            score += 25
            reasons.append("Same category")

        
        if (
            candidate_package.lower()
            == target_package.lower()
        ):
            score += 25
            reasons.append("Same package")

        try:
            candidate_voltage = float(
                candidate["voltage"]
            )

            if abs(
                candidate_voltage - target_voltage
            ) <= 0.5:

                score += 20
                reasons.append("Voltage compatible")

        except (ValueError, TypeError):
            pass

        try:
            candidate_current = float(
                candidate["current"]
            )

            if target_current > 0:

                current_difference = abs(
                    candidate_current - target_current
                )

                current_tolerance = (
                    target_current * 0.10
                )

                if current_difference <= current_tolerance:
                    score += 20
                    reasons.append(
                        "Current compatible"
                    )

        except (ValueError, TypeError):
            pass

        candidate_tolerance = str(
            candidate["tolerance"]
        ).strip()

        if (
            candidate_tolerance
            == target_tolerance
        ):
            score += 10
            reasons.append(
                "Tolerance compatible"
            )

        if score > best_score:

            best_score = score

            best_component = {
                "part_number": candidate[
                    "part_number"
                ],
                "score": score,
                "reason": ", ".join(reasons)
            }

    if best_component is None:

        return {
            "best_alternative": None,
            "compatibility_percentage": 0,
            "alternative_type":
                "No Suitable Alternative",
            "reason":
                "No compatible substitute found."
        }

    if best_score == 100:

        recommendation_type = "Exact Drop-in"

    elif best_score >= 70:

        recommendation_type = "Minor Redesign"

    else:

        recommendation_type = "Requires Redesign"

    return {
        "best_alternative":
            best_component["part_number"],

        "compatibility_percentage":
            best_score,

        "alternative_type":
            recommendation_type,

        "reason":
            best_component["reason"]
    }