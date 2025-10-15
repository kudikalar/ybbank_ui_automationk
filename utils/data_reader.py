import pandas as pd
from pathlib import Path
from typing import Union


def read_excel(file_path: str, sheet_name: Union[str, int] = 0):
    """
    Read exactly ONE sheet and return list[dict].
    Fails if sheet_name is None or a list.
    """
    if sheet_name is None:
        raise ValueError("sheet_name cannot be None. Pass a sheet NAME (str) or INDEX (int).")
    if isinstance(sheet_name, (list, tuple)):
        raise ValueError("Pass a single sheet, not multiple. Got a list/tuple.")

    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Excel file not found: {file_path}")

    df = pd.read_excel(path, sheet_name=sheet_name, engine="openpyxl")
    # Safety: pandas returns a dict only if None/list was passed
    if isinstance(df, dict):
        raise RuntimeError("Multiple sheets were loaded unexpectedly. Ensure sheet_name is str/int.")
    return df.to_dict(orient="records")