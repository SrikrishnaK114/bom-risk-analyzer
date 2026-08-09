from services.bom_parser import parse_bom
from services.enricher import enrich_bom
from services.analyzer import analyze_component


def analyze_bom(bom_file):
    """
    Complete BOM analysis pipeline.

    Flow:
        BOM CSV
            ↓
        Parse
            ↓
        Enrich using component master
            ↓
        Risk + substitute + AI analysis
            ↓
        Sort by risk
    """

    # 1. Parse user's BOM
    parsed_bom = parse_bom(bom_file)

    # 2. Enrich parsed components
    enriched_bom = enrich_bom(
        parsed_bom["components"]
    )

    # 3. Analyze every enriched component
    results = []

    for component in enriched_bom["components"]:
        result = analyze_component(component)
        results.append(result)

    # 4. Highest risk first
    results = sorted(
        results,
        key=lambda x: x["risk_analysis"]["score"],
        reverse=True
    )

    return {
        "total_components": len(results),
        "risk_ranked_components": results
    }

if __name__ == "__main__":

    result = analyze_bom(
        "data/sample_bom.csv"
    )

    import json

    print(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False
        )
    )