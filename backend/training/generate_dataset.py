import pandas as pd
import random
from pathlib import Path

components = [
    {
        "part_number": "STM32F103C8",
        "category": "MCU",
        "package": "LQFP48",
        "voltage": 3.3,
        "current": 0.05,
        "tolerance": "±5%",
        "alternative": "GD32F103CBT6",
        "alt_type": "Minor Redesign"
    },

    {
        "part_number": "LM7805",
        "category": "Voltage Regulator",
        "package": "TO220",
        "voltage": 5,
        "current": 1,
        "tolerance": "±5%",
        "alternative": "LM1117-5.0",
        "alt_type": "Drop-in"
    },

    {
        "part_number": "IRF540N",
        "category": "MOSFET",
        "package": "TO220",
        "voltage": 100,
        "current": 33,
        "tolerance": "±10%",
        "alternative": "IRLZ44N",
        "alt_type": "Minor Redesign"
    },

    {
        "part_number": "ESP32-WROOM",
        "category": "WiFi Module",
        "package": "Module",
        "voltage": 3.3,
        "current": 0.5,
        "tolerance": "±5%",
        "alternative": "ESP32-S3-WROOM-1",
        "alt_type": "Minor Redesign"
    },

    {
        "part_number": "MPU6050",
        "category": "Sensor",
        "package": "QFN24",
        "voltage": 3.3,
        "current": 0.004,
        "tolerance": "±5%",
        "alternative": "ICM42688P",
        "alt_type": "Major Redesign"
    }
]
lifecycles = ["Active", "NRND", "EOL"]
criticalities = ["Low", "Medium", "High"]

rows = []

for i in range(500):

    component = random.choice(components)

    lifecycle = random.choices(
        lifecycles,
        weights=[70, 20, 10]
    )[0]

    criticality = random.choice(criticalities)

    second_source = random.choice([True, False])

    lead_time = random.randint(4, 28)

    availability = random.randint(500, 50000)

    risk = 0

    # Lifecycle contribution
    if lifecycle == "Active":
        risk += 5
    elif lifecycle == "NRND":
        risk += 35
    else:  # EOL
        risk += 60

    # Lead time contribution
    if lead_time > 20:
        risk += 20
    elif lead_time > 12:
        risk += 10

    # Availability contribution
    if availability < 5000:
        risk += 20
    elif availability < 15000:
        risk += 10

    # Criticality contribution
    if criticality == "High":
        risk += 15
    elif criticality == "Medium":
        risk += 8

    # Single source contribution
    if not second_source:
        risk += 10

    # Small random variation
    risk += random.randint(-3, 3)

    # Keep between 0 and 100
    risk = max(0, min(100, risk))
    rows.append({
        "part_number": component["part_number"],
        "category": component["category"],
        "package": component["package"],
        "voltage": component["voltage"],
        "current": component["current"],
        "tolerance": component["tolerance"],
        "criticality": criticality,
        "second_source": second_source,
        "lifecycle": lifecycle,
        "lead_time_weeks": lead_time,
        "availability": availability,
        "overall_risk": risk,
        "best_alternative": component["alternative"],
        "alternative_type": component["alt_type"]
    })
df = pd.DataFrame(rows)

output_file = Path(__file__).parent / "component_dataset.csv"

df.to_csv(output_file, index=False)

print("Dataset generated successfully!")
print(df.head())