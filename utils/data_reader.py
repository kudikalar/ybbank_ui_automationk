import pandas as pd
from pathlib import Path

def read_excel(file_path: str, sheet_name: str = 0):
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Excel file not found: {file_path}")
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    return df.to_dict(orient="records")
