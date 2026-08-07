from services.analyzer import analyze_component


component = {

    "part_number": "STM32F103C8",

    "category": "MCU",

    "package": "LQFP48",

    "criticality": "High",

    "second_source": False,

    "lifecycle": "NRND",

    "lead_time": 20,

    "availability": 3000,

    "electrical_specs": {
        "voltage": "3.3V",
        "current": "50mA",
        "tolerance": "±5%"
    }
}


result = analyze_component(component)


print("\n========== FINAL BOM ANALYSIS ==========\n")

print("\nComponent:")
print(result["component"])


print("\nRisk Analysis:")
print(result["risk_analysis"])


print("\nRecommendation:")
print(result["substitute_recommendation"])


print("\nAI Explanation:")
print(result["ai_explanation"])