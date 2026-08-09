from services.risk_engine import calculate_component_risk
from services.recommender import find_best_substitute
from services.llm_service import generate_component_explanation



def analyze_component(component):
    
    # 1. Predict risk using ML model
    risk_result = calculate_component_risk(component)


    # 2. Find substitute component
    recommendation = find_best_substitute(component)


    # 3. Generate AI explanation
    explanation = generate_component_explanation(
        component,
        risk_result,
        recommendation
    )


    return {

    "component": {
        "part_number": component.get("part_number"),
        "category": component.get("category"),
        "criticality": component.get("criticality")
    },


    "risk_analysis": {

        "score": risk_result.get("risk_score"),

        "level": risk_result.get("risk_level"),

        "factors": risk_result.get("risk_breakdown")
    },


    "substitute_recommendation": {

        "part_number": recommendation.get("best_alternative"),

        "compatibility_percentage": recommendation.get(
            "compatibility_percentage"
        ),

        "alternative_type": recommendation.get(
            "alternative_type"
        ),

        "reason": recommendation.get(
            "reason"
        )
    },


    "ai_explanation": explanation

}