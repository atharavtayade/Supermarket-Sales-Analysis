"""
Data Cleaning Module
====================
Handles data cleaning and preprocessing for the supermarket sales dataset.
"""

import pandas as pd
import numpy as np
from typing import Tuple, Optional


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names by stripping whitespace.
    
    Parameters
    ----------
    df : pd.DataFrame
        Raw dataset.
    
    Returns
    -------
    pd.DataFrame
        DataFrame with cleaned column names.
    """
    df = df.copy()
    df.columns = df.columns.str.strip()
    return df


def check_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze missing values in the dataset.

    Parameters
    ----------
    df : pd.DataFrame
        The dataset to check.

    Returns
    -------
    pd.DataFrame
        Summary of missing values per column with count and percentage.
    """
    missing_count = df.isnull().sum()
    missing_pct = (missing_count / len(df) * 100).round(2)
    summary = pd.DataFrame({
        "Missing Count": missing_count,
        "Missing %": missing_pct
    })
    return summary[summary["Missing Count"] > 0].sort_values(
        "Missing Count", ascending=False
    )


def remove_duplicates(df: pd.DataFrame, subset: Optional[list] = None) -> Tuple[pd.DataFrame, int]:
    """
    Remove duplicate rows from the dataset.

    Parameters
    ----------
    df : pd.DataFrame
        The dataset.
    subset : list, optional
        Columns to consider for identifying duplicates.
        If None, all columns are used.

    Returns
    -------
    tuple of (pd.DataFrame, int)
        Cleaned DataFrame and number of duplicates removed.
    """
    initial_count = len(df)
    df_clean = df.drop_duplicates(subset=subset).reset_index(drop=True)
    removed = initial_count - len(df_clean)
    return df_clean, removed


def convert_date_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Parse the 'Date' column to datetime and extract temporal features.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset with a 'Date' column.

    Returns
    -------
    pd.DataFrame
        Dataset with parsed Date and new temporal columns.
    """
    df = df.copy()

    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], format="mixed", dayfirst=False)
        df["Day"] = df["Date"].dt.day
        df["Month"] = df["Date"].dt.month
        df["Month_Name"] = df["Date"].dt.month_name()
        df["Day_of_Week"] = df["Date"].dt.day_name()
        df["Week_Number"] = df["Date"].dt.isocalendar().week.astype(int)

    return df


def convert_time_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Parse the 'Time' column and extract hour information.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset with a 'Time' column.

    Returns
    -------
    pd.DataFrame
        Dataset with parsed Time and 'Hour' column.
    """
    df = df.copy()

    if "Time" in df.columns:
        df["Time"] = pd.to_datetime(df["Time"], format="mixed").dt.time
        df["Hour"] = df["Time"].apply(lambda x: x.hour if pd.notna(x) else np.nan)

    return df


def validate_numerical_ranges(df: pd.DataFrame) -> dict:
    """
    Validate numerical columns for suspicious values.

    Parameters
    ----------
    df : pd.DataFrame
        The dataset to validate.

    Returns
    -------
    dict
        Dictionary of columns with suspicious values and their details.
    """
    issues = {}

    # Unit price should be positive
    if "Unit price" in df.columns:
        invalid = df[df["Unit price"] <= 0]
        if len(invalid) > 0:
            issues["Unit price <= 0"] = len(invalid)

    # Quantity should be positive integer
    if "Quantity" in df.columns:
        invalid = df[df["Quantity"] <= 0]
        if len(invalid) > 0:
            issues["Quantity <= 0"] = len(invalid)

    # Total should be positive
    if "Total" in df.columns:
        invalid = df[df["Total"] <= 0]
        if len(invalid) > 0:
            issues["Total <= 0"] = len(invalid)

    # Rating should be between 1 and 10
    if "Rating" in df.columns:
        invalid = df[(df["Rating"] < 1) | (df["Rating"] > 10)]
        if len(invalid) > 0:
            issues["Rating outside 1-10"] = len(invalid)

    # Tax should be non-negative
    if "Tax 5%" in df.columns:
        invalid = df[df["Tax 5%"] < 0]
        if len(invalid) > 0:
            issues["Tax 5% < 0"] = len(invalid)

    return issues


def validate_categorical_values(df: pd.DataFrame) -> dict:
    """
    Validate categorical columns for unexpected values.

    Parameters
    ----------
    df : pd.DataFrame
        The dataset.

    Returns
    -------
    dict
        Expected vs actual unique values for key categorical columns.
    """
    expected = {
        "Branch": {"A", "B", "C"},
        "City": {"Yangon", "Naypyitaw", "Mandalay"},
        "Customer type": {"Member", "Normal"},
        "Gender": {"Male", "Female"},
        "Payment": {"Cash", "Ewallet", "Credit card"},
        "Product line": {
            "Health and beauty", "Electronic accessories",
            "Home and lifestyle", "Sports and travel",
            "Food and beverages", "Fashion accessories"
        }
    }

    report = {}
    for col, expected_vals in expected.items():
        if col in df.columns:
            actual_vals = set(df[col].dropna().unique())
            unexpected = actual_vals - expected_vals
            if unexpected:
                report[col] = {
                    "expected": expected_vals,
                    "unexpected": unexpected
                }

    return report


def clean_dataset(df: pd.DataFrame) -> Tuple[pd.DataFrame, dict]:
    """
    Execute the full cleaning pipeline on the raw dataset.

    Parameters
    ----------
    df : pd.DataFrame
        Raw dataset.

    Returns
    -------
    tuple of (pd.DataFrame, dict)
        Cleaned DataFrame and a cleaning report dictionary.
    """
    report = {}

    # Step 1: Clean column names
    df_clean = clean_column_names(df)
    report["original_shape"] = df_clean.shape

    # Step 2: Check missing values
    missing_summary = check_missing_values(df_clean)
    report["missing_values"] = missing_summary

    # Step 3: Remove duplicates
    df_clean, dup_count = remove_duplicates(df_clean)
    report["duplicates_removed"] = dup_count
    report["shape_after_dedup"] = df_clean.shape

    # Step 4: Convert date columns
    df_clean = convert_date_columns(df_clean)

    # Step 5: Convert time column
    df_clean = convert_time_column(df_clean)

    # Step 6: Validate numerical ranges
    numerical_issues = validate_numerical_ranges(df_clean)
    report["numerical_issues"] = numerical_issues

    # Step 7: Validate categorical values
    categorical_issues = validate_categorical_values(df_clean)
    report["categorical_issues"] = categorical_issues

    # Step 8: Ensure correct numeric types
    numeric_cols = ["Unit price", "Quantity", "Tax 5%", "Total", "cogs",
                    "gross margin percentage", "gross income", "Rating"]
    for col in numeric_cols:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")

    report["final_shape"] = df_clean.shape
    report["final_dtypes"] = df_clean.dtypes

    return df_clean, report


def print_cleaning_report(report: dict) -> None:
    """Print a formatted cleaning report."""
    print("=" * 60)
    print("DATA CLEANING REPORT")
    print("=" * 60)
    print(f"\nOriginal Shape: {report['original_shape']}")
    print(f"Duplicates Removed: {report['duplicates_removed']}")
    print(f"Shape After Dedup: {report['shape_after_dedup']}")
    print(f"Final Shape: {report['final_shape']}")

    if report["missing_values"].empty:
        print("\nMissing Values: None found")
    else:
        print("\n--- Missing Values ---")
        print(report["missing_values"].to_string())

    if report["numerical_issues"]:
        print("\n--- Numerical Issues ---")
        for issue, count in report["numerical_issues"].items():
            print(f"  {issue}: {count} rows")
    else:
        print("\nNumerical Validation: All values within expected ranges")

    if report["categorical_issues"]:
        print("\n--- Categorical Issues ---")
        for col, info in report["categorical_issues"].items():
            print(f"  {col}: unexpected values {info['unexpected']}")
    else:
        print("\nCategorical Validation: All values within expected categories")

    print("=" * 60)
