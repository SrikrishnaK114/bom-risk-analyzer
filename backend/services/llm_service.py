import os
from dotenv import load_dotenv
from groq import Groq


load_dotenv()


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_component_explanation(component, risk_result, recommendation):

    prompt = f"""
You are an electronics supply chain risk analyst.

Analyze this BOM component.
Do not invent manufacturer details, datasheet information, or lifecycle announcements.
Explain risks based on the given fields only.
Component:
{component}

Risk Analysis:
{risk_result}

Alternative Recommendation:
{recommendation}

Generate:

1. Risk explanation
2. Main contributing factors
3. Recommended engineering action

Keep it concise and technical.
"""


    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You analyze electronic component obsolescence and supply chain risks."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )


    return response.choices[0].message.content