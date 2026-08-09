import pandas as pd

REQUIRED_COLUMNS = [
    "part_number",
    "manufacturer",
    "quantity"
]


def parse_bom(file_path):
   
    df = pd.read_csv(file_path)

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
    )

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Invalid BOM: missing required column(s): "
            + ", ".join(missing_columns)
        )

    components = []

    for index, row in df.iterrows():

        part_number = row["part_number"]

        if pd.isna(part_number) or str(part_number).strip() == "":
            raise ValueError(
                f"Invalid BOM: row {index + 2} has an empty part_number."
            )

        part_number = str(part_number).strip()

        manufacturer = row["manufacturer"]

        if (
            pd.isna(manufacturer)
            or str(manufacturer).strip() == ""
        ):
            raise ValueError(
                f"Invalid BOM: row {index + 2} has an empty manufacturer."
            )

        manufacturer = str(manufacturer).strip()

        quantity = row["quantity"]

        if pd.isna(quantity) or str(quantity).strip() == "":
            raise ValueError(
                f"Invalid BOM: row {index + 2} has an empty quantity."
            )

        try:
            quantity = int(float(quantity))
        except (ValueError, TypeError):
            raise ValueError(
                f"Invalid BOM: row {index + 2} has an invalid quantity."
            )

        if quantity <= 0:
            raise ValueError(
                f"Invalid BOM: row {index + 2} quantity "
                "must be greater than 0."
            )

        category = row.get("category")

        if pd.isna(category) or str(category).strip() == "":
            category = None
        else:
            category = str(category).strip()

        package = row.get("package")

        if pd.isna(package) or str(package).strip() == "":
            package = None
        else:
            package = str(package).strip()

        criticality = row.get("criticality")

        if (
            pd.isna(criticality)
            or str(criticality).strip() == ""
        ):
            criticality = "Unknown"
        else:
            criticality = str(criticality).strip()

        second_source = row.get("second_source")

        if (
            pd.isna(second_source)
            or str(second_source).strip() == ""
        ):
            second_source = False

        else:
            value = str(second_source).strip().lower()

            if value in ["true", "yes", "y", "1"]:
                second_source = True

            elif value in ["false", "no", "n", "0"]:
                second_source = False

            else:
                raise ValueError(
                    f"Invalid BOM: row {index + 2} has an invalid "
                    f"second_source value: '{second_source}'."
                )

        component = {
            "part_number": part_number,
            "manufacturer": manufacturer,
            "category": category,
            "package": package,
            "qty": quantity,
            "criticality": criticality,
            "second_source": second_source
        }

        components.append(component)

    return {
        "components": components
    }


if __name__ == "__main__":

    bom = parse_bom("backend/data/sample_bom.csv")

    print("\n========== PARSED BOM ==========\n")

    for component in bom["components"]:
        print(component)