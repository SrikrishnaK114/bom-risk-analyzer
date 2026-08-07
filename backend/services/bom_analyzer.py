import pandas as pd

from services.analyzer import analyze_component



def analyze_bom(bom_file):

    """
    Analyze complete BOM.

    Input:
        CSV file path

    Output:
        Ranked component risk report
    """


    bom = pd.read_csv(bom_file)


    results = []


    for _, row in bom.iterrows():

        component = {

            "part_number": row["part_number"],

            "qty": row.get("qty", 1)

        }


        # Analyze each component
        result = analyze_component(component)


        results.append(result)



    # Sort highest risk first

    results = sorted(
        results,
        key=lambda x: x["risk_analysis"]["score"],
        reverse=True
    )


    return {

        "total_components": len(results),

        "risk_ranked_components": results

    }