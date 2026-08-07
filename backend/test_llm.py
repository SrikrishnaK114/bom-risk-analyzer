from services.llm_service import generate_component_explanation


component = {
    "part_number": "STM32F103C8",
    "category": "MCU",
    "package": "LQFP48",
    "lifecycle": "NRND",
    "lead_time": 20,
    "availability": 3000,
    "second_source": False
}


risk_result = {
    "risk_score": 78,
    "risk_level": "High"
}


recommendation = {
    "best_alternative": "STM32F103CBT6",
    "compatibility_percentage": 100,
    "alternative_type": "Exact Drop-in"
}


response = generate_component_explanation(
    component,
    risk_result,
    recommendation
)


print("\nAI Explanation:")
print(response)