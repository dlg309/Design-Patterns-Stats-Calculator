"""Read observations from CSV files without performing calculations."""

from pathlib import Path

import pandas as pd


def read_csv_values(path, *, column="value"):
    frame = pd.read_csv(Path(path))

    if column not in frame.columns:
        raise ValueError(f"CSV must contain a column named {column}.")

    return frame[column].tolist()
