import json

from services.risk_engine import calculate_component_risk

with open("data/sample_components.json") as file:

    data = json.load(file)

for component in data["components"]:

    result = calculate_component_risk(component)

    print(result)