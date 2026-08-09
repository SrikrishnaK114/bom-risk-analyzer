from fastapi import FastAPI, UploadFile, File, HTTPException
import tempfile
import os

from services.bom_analyzer import analyze_bom


app = FastAPI(
    title="BOM Risk Analyzer",
    description="BOM risk analysis and substitute recommendation API"
)


@app.get("/")
def root():
    return {
        "message": "BOM Risk Analyzer API is running"
    }


@app.post("/analyze")
async def analyze_uploaded_bom(
    file: UploadFile = File(...)
):

    # Only CSV files are accepted
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a CSV BOM file."
        )

    temp_path = None

    try:

        # Save uploaded BOM temporarily
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".csv"
        ) as temp_file:

            contents = await file.read()

            temp_file.write(contents)

            temp_path = temp_file.name

        # Run YOUR complete backend pipeline
        result = analyze_bom(temp_path)

        return result

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:

        # Remove temporary BOM
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)