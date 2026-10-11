"""
Data Loader Module
==================
Handles loading the supermarket sales dataset with validation and error reporting.
"""

import os
import pandas as pd
import numpy as np
from typing import Optional, Tuple


# Expected columns in the Kaggle Supermarket Sales dataset
EXPECTED_COLUMNS = [
    "Invoice ID", "Branch", "City", "Customer type", "Gender",
    "Product line", "Unit price", "Quantity", "Tax 5%", "Total",
    "Date", "Time", "Payment", "cogs", "gross margin percentage",
    "gross income", "Rating"
]

# Default data path
DEFAULT_DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "supermarket_sales.csv"
)


def load_dataset(filepath: Optional[str] = None) -> pd.DataFrame:
    """
    Load the supermarket sales dataset from a CSV file.

    Parameters
    ----------
    filepath : str, optional
        Path to the CSV file. Defaults to data/supermarket_sales.csv.

    Returns
    -------
    pd.DataFrame
        The loaded dataset.

    Raises
    ------
    FileNotFoundError
        If the dataset file does not exist at the specified path.
    ValueError
        If the file is empty or cannot be parsed.
    """
    if filepath is None:
        filepath = DEFAULT_DATA_PATH

    # Check file existence
    if not os.path.isfile(filepath):
        raise FileNotFoundError(
            f"Dataset not found at: {filepath}\n"
            f"Please download the dataset from:\n"
            f"  https://www.kaggle.com/datasets/aungpyaeap/supermarket-sales\n"
            f"and place the CSV file in the data/ directory."
        )

    # Check file size
    if os.path.getsize(filepath) == 0:
        raise ValueError(f"Dataset file is empty: {filepath}")

    # Load the CSV
    try:
        df = pd.read_csv(filepath)
    except Exception as e:
        raise ValueError(f"Failed to parse dataset at {filepath}: {e}")

    if df.empty:
        raise ValueError("Dataset loaded but contains no rows.")

    return df


def inspect_dataset(df: pd.DataFrame) -> dict:
    """
    Perform initial inspection of the loaded dataset.

    Parameters
    ----------
    df : pd.DataFrame
        The loaded dataset.

    Returns
    -------
    dict
        Dictionary containing inspection results:
        - shape: (rows, columns)
        - columns: list of column names
        - dtypes: Series of data types
        - missing_values: Series of missing value counts
        - missing_pct: Series of missing value percentages
        - duplicates: number of duplicate rows
        - sample: first 5 rows
        - memory_usage: total memory in MB
    """
    results = {
        "shape": df.shape,
        "columns": df.columns.tolist(),
        "dtypes": df.dtypes,
        "missing_values": df.isnull().sum(),
        "missing_pct": (df.isnull().sum() / len(df) * 100).round(2),
        "duplicates": df.duplicated().sum(),
        "sample": df.head(),
        "memory_usage": df.memory_usage(deep=True).sum() / (1024 * 1024),
    }
    return results


def validate_schema(df: pd.DataFrame, expected_columns: list = None) -> Tuple[bool, list, list]:
    """
    Validate that the dataset contains the expected columns.

    Parameters
    ----------
    df : pd.DataFrame
        The loaded dataset.
    expected_columns : list, optional
        List of expected column names. Defaults to EXPECTED_COLUMNS.

    Returns
    -------
    tuple of (bool, list, list)
        - is_valid: True if all expected columns are present
        - missing: columns expected but not found
        - extra: columns found but not expected
    """
    if expected_columns is None:
        expected_columns = EXPECTED_COLUMNS

    actual = set(df.columns.tolist())
    expected = set(expected_columns)

    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    is_valid = len(missing) == 0

    return is_valid, missing, extra


def print_inspection_report(results: dict) -> None:
    """Print a formatted inspection report to stdout."""
    print("=" * 60)
    print("DATASET INSPECTION REPORT")
    print("=" * 60)
    print(f"\nShape: {results['shape'][0]} rows × {results['shape'][1]} columns")
    print(f"Memory Usage: {results['memory_usage']:.2f} MB")
    print(f"Duplicate Rows: {results['duplicates']}")

    print("\n--- Column Data Types ---")
    print(results["dtypes"].to_string())

    print("\n--- Missing Values ---")
    missing = results["missing_values"]
    if missing.sum() == 0:
        print("No missing values found.")
    else:
        missing_info = pd.DataFrame({
            "Missing": missing[missing > 0],
            "Pct (%)": results["missing_pct"][missing > 0]
        })
        print(missing_info.to_string())

    print("\n--- Sample Data (First 5 Rows) ---")
    print(results["sample"].to_string())
    print("=" * 60)
