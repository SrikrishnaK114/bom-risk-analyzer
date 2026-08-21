import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_component_explanation(
    component,
    risk_result,
    recommendation
):

    prompt = f"""
You are an electronics supply chain risk analyst.

Analyze ONLY the information provided below.

IMPORTANT RULES:
- The ML risk score is the overall risk score. Do not recalculate it.
- The risk level is based on the ML risk score.
- "criticality" means how important the component is to the system.
- High criticality does NOT automatically mean High overall risk.
- Treat each risk factor separately:
  obsolescence, supply, single_source, and criticality.
- Do not invent any information.
- Do not claim anything about manufacturer history, datasheets,
  market conditions, lifecycle announcements, or technical behavior
  that is not explicitly provided.
- Do not change the compatibility percentage.
- Do not describe "compatible" specifications as "identical".
- Do not claim an alternative is electrically or mechanically verified.
- Use the recommendation exactly as provided.

Component:
{component}

Risk Analysis:
{risk_result}

Alternative Recommendation:
{recommendation}

Generate exactly these sections:

1. Risk Explanation
2. Main Contributing Factors
3. Recommended Engineering Action

Keep the explanation concise and technical.
"""
    response = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You analyze electronic component "
                    "obsolescence and supply-chain risks. "
                    "You must follow the supplied numerical "
                    "risk analysis exactly."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content