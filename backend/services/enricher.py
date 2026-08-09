from pathlib import Path
import json

import pandas as pd

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

def enrich_component(component):
    
    part_number = str(
        component.get("part_number", "")
    ).strip()

    if not part_number:
        raise ValueError(
            "Cannot enrich component: missing part_number."
        )

    match = component_db[
        component_db["part_number"].str.upper()
        == part_number.upper()
    ]

    if match.empty:
        raise ValueError(
            f"Component '{part_number}' was not found "
            "in component_master_final.csv."
        )

    master = match.iloc[0]

    voltage = float(master["voltage"])

    current_amps = float(master["current"])
    current_ma = current_amps * 1000

    if current_ma.is_integer():
        current_string = f"{int(current_ma)}mA"
    else:
        current_string = f"{current_ma:g}mA"

    second_source_value = (
        str(master["second_source"])
        .strip()
        .lower()
    )

    second_source = second_source_value in {
        "yes",
        "true",
        "1"
    }

    criticality = component.get("criticality")

    if (
        criticality is None
        or pd.isna(criticality)
        or str(criticality).strip() == ""
        or str(criticality).strip().lower() == "unknown"
    ):
        criticality = str(
            master["criticality"]
        ).strip()
    else:
        criticality = str(criticality).strip()

    enriched_component = {
        "part_number": part_number,

        "category": str(
            master["category"]
        ).strip(),

        "package": str(
            master["package"]
        ).strip(),

        "qty": int(
            component.get("qty", 1)
        ),

        "criticality": criticality,

        "second_source": second_source,

        "manufacturer": str(
            master["manufacturer"]
        ).strip(),

        "lifecycle": str(
            master["lifecycle"]
        ).strip(),

        "lead_time": int(
            master["lead_time"]
        ),

        "availability": int(
            master["availability"]
        ),

        "electrical_specs": {
            "voltage": f"{voltage:g}V",

            "current": current_string,

            "tolerance": str(
                master["tolerance"]
            ).strip()
        }
    }

    return enriched_component


def enrich_bom(components):
    
    enriched_components = []

    for component in components:
        enriched_components.append(
            enrich_component(component)
        )

    return {
        "components": enriched_components
    }

if __name__ == "__main__":

    print("\n========================================")
    print("ENRICHMENT TEST")
    print("========================================")

    print("\nDatabase:")
    print(DATASET_PATH)

    print(
        f"\nComponents in database: "
        f"{len(component_db)}"
    )

    sample_components = [
        {
            "part_number": "STM32F103C8",
            "manufacturer": "STMicroelectronics",
            "qty": 2
        },
        {
            "part_number": "STM32F103CBT6",
            "manufacturer": "STMicroelectronics",
            "qty": 1
        },
        {
            "part_number": "GD32F103CBT6",
            "manufacturer": "GigaDevice",
            "qty": 3
        }
    ]

    result = enrich_bom(sample_components)

    print("\n========================================")
    print("ENRICHED BOM")
    print("========================================\n")

    print(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False
        )
    )