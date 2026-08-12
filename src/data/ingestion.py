from pathlib import Path
import hashlib

import pandas as pd


def load_data(file_path: str | Path) -> pd.DataFrame:
    """Load the raw household dataset."""

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    df = pd.read_csv(path)

    if df.empty:
        raise ValueError("Dataset is empty.")

    return df


def calculate_file_hash(file_path: str | Path) -> str:
    """Calculate SHA256 hash for dataset version tracking."""

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for block in iter(lambda: file.read(4096), b""):
            sha256.update(block)

    return sha256.hexdigest()
