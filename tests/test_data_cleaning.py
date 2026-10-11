"""
Tests for data_cleaning module.
Uses small synthetic DataFrames to validate cleaning functions.
"""

import pytest
import pandas as pd
import numpy as np
import sys
import os

# Ensure project root is on the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_cleaning import (
    clean_column_names,
    check_missing_values,
    remove_duplicates,
    convert_date_columns,
    convert_time_column,
    validate_numerical_ranges,
    validate_categorical_values,
    clean_dataset
)


# ── Fixtures ───────────────────────────────────────────────

@pytest.fixture
def sample_df():
    """Create a small synthetic dataset mimicking the supermarket sales schema."""
    return pd.DataFrame({
        "Invoice ID": ["750-67-8428", "226-31-3081", "631-41-3108", "123-45-6789"],
        "Branch": ["A", "C", "A", "B"],
        "City": ["Yangon", "Naypyitaw", "Yangon", "Mandalay"],
        "Customer type": ["Member", "Normal", "Normal", "Member"],
        "Gender": ["Female", "Female", "Male", "Male"],
        "Product line": [
            "Health and beauty", "Electronic accessories",
            "Home and lifestyle", "Food and beverages"
        ],
        "Unit price": [74.69, 15.28, 46.33, 58.22],
        "Quantity": [7, 5, 7, 8],
        "Tax 5%": [26.14, 3.82, 16.22, 23.29],
        "Total": [548.97, 80.22, 340.53, 489.05],
        "Date": ["1/5/2019", "3/8/2019", "3/3/2019", "1/27/2019"],
        "Time": ["13:08", "10:29", "13:23", "20:33"],
        "Payment": ["Ewallet", "Cash", "Credit card", "Ewallet"],
        "cogs": [522.83, 76.40, 324.31, 465.76],
        "gross margin percentage": [4.761905] * 4,
        "gross income": [26.14, 3.82, 16.22, 23.29],
        "Rating": [9.1, 9.6, 7.4, 8.4]
    })


@pytest.fixture
def df_with_duplicates(sample_df):
    """Create dataset with duplicate rows."""
    return pd.concat([sample_df, sample_df.iloc[:2]], ignore_index=True)


@pytest.fixture
def df_with_missing():
    """Create dataset with missing values."""
    return pd.DataFrame({
        "Invoice ID": ["A", "B", "C", "D"],
        "Branch": ["A", None, "C", "A"],
        "Total": [100.0, np.nan, 200.0, 300.0],
        "Rating": [7.5, 8.0, np.nan, 6.5],
        "Date": ["1/1/2019", "2/1/2019", None, "3/1/2019"],
        "Time": ["10:00", None, "12:00", "14:00"],
    })


@pytest.fixture
def empty_df():
    """Create an empty DataFrame."""
    return pd.DataFrame()


# ── Tests: clean_column_names ─────────────────────────────

def test_clean_column_names_strips_whitespace():
    df = pd.DataFrame({" Name ": [1], "  Value": [2], "Score  ": [3]})
    result = clean_column_names(df)
    assert list(result.columns) == ["Name", "Value", "Score"]


def test_clean_column_names_no_modification(sample_df):
    result = clean_column_names(sample_df)
    assert list(result.columns) == list(sample_df.columns)


# ── Tests: check_missing_values ───────────────────────────

def test_check_missing_no_missing(sample_df):
    result = check_missing_values(sample_df)
    assert result.empty


def test_check_missing_with_missing(df_with_missing):
    result = check_missing_values(df_with_missing)
    assert len(result) > 0
    assert "Branch" in result.index
    assert "Total" in result.index


# ── Tests: remove_duplicates ─────────────────────────────

def test_remove_duplicates_with_dupes(df_with_duplicates):
    result, removed = remove_duplicates(df_with_duplicates)
    assert removed == 2
    assert len(result) == 4


def test_remove_duplicates_no_dupes(sample_df):
    result, removed = remove_duplicates(sample_df)
    assert removed == 0
    assert len(result) == len(sample_df)


# ── Tests: convert_date_columns ──────────────────────────

def test_convert_date_columns(sample_df):
    result = convert_date_columns(sample_df)
    assert pd.api.types.is_datetime64_any_dtype(result["Date"])
    assert "Day" in result.columns
    assert "Month" in result.columns
    assert "Month_Name" in result.columns
    assert "Day_of_Week" in result.columns
    assert "Week_Number" in result.columns


def test_convert_date_no_date_column():
    df = pd.DataFrame({"A": [1, 2, 3]})
    result = convert_date_columns(df)
    assert "Day" not in result.columns


# ── Tests: convert_time_column ───────────────────────────

def test_convert_time_column(sample_df):
    result = convert_time_column(sample_df)
    assert "Hour" in result.columns
    assert result["Hour"].iloc[0] == 13


def test_convert_time_no_time_column():
    df = pd.DataFrame({"A": [1, 2, 3]})
    result = convert_time_column(df)
    assert "Hour" not in result.columns


# ── Tests: validate_numerical_ranges ─────────────────────

def test_validate_numerical_no_issues(sample_df):
    issues = validate_numerical_ranges(sample_df)
    assert len(issues) == 0


def test_validate_numerical_negative_price():
    df = pd.DataFrame({
        "Unit price": [-5.0, 10.0],
        "Quantity": [1, 2],
        "Total": [100, 200],
        "Rating": [5.0, 8.0],
        "Tax 5%": [5, 10],
    })
    issues = validate_numerical_ranges(df)
    assert "Unit price <= 0" in issues


def test_validate_numerical_bad_rating():
    df = pd.DataFrame({
        "Rating": [0.5, 11.0, 7.0],
    })
    issues = validate_numerical_ranges(df)
    assert "Rating outside 1-10" in issues
    assert issues["Rating outside 1-10"] == 2


# ── Tests: validate_categorical_values ───────────────────

def test_validate_categorical_valid(sample_df):
    issues = validate_categorical_values(sample_df)
    assert len(issues) == 0


def test_validate_categorical_invalid():
    df = pd.DataFrame({
        "Branch": ["A", "B", "X"],
        "Payment": ["Cash", "Bitcoin", "Ewallet"],
    })
    issues = validate_categorical_values(df)
    assert "Branch" in issues
    assert "X" in issues["Branch"]["unexpected"]
    assert "Payment" in issues
    assert "Bitcoin" in issues["Payment"]["unexpected"]


# ── Tests: clean_dataset ─────────────────────────────────

def test_clean_dataset_full_pipeline(sample_df):
    df_clean, report = clean_dataset(sample_df)
    assert report["duplicates_removed"] == 0
    assert report["final_shape"][0] == 4
    assert "Day" in df_clean.columns
    assert "Hour" in df_clean.columns


def test_clean_dataset_with_duplicates(df_with_duplicates):
    df_clean, report = clean_dataset(df_with_duplicates)
    assert report["duplicates_removed"] == 2
    assert len(df_clean) == 4


# ── Tests: edge cases ────────────────────────────────────

def test_empty_dataframe():
    df = pd.DataFrame()
    missing = check_missing_values(df)
    assert missing.empty


def test_single_row():
    df = pd.DataFrame({
        "Invoice ID": ["001"],
        "Branch": ["A"],
        "Total": [100.0],
        "Date": ["1/1/2019"],
        "Time": ["10:00"],
        "Rating": [7.5],
    })
    df_clean, report = clean_dataset(df)
    assert report["duplicates_removed"] == 0
    assert report["final_shape"][0] == 1
