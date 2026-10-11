"""
Tests for analysis module.
Uses small synthetic DataFrames to validate analytical functions.
"""

import pytest
import pandas as pd
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.analysis import (
    compute_overall_metrics,
    sales_by_group,
    product_line_analysis,
    branch_analysis,
    customer_analysis,
    payment_analysis,
    time_analysis,
    rating_analysis,
    correlation_analysis,
    generate_summary_table
)


# ── Fixtures ───────────────────────────────────────────────

@pytest.fixture
def sample_df():
    """Create a synthetic cleaned dataset for testing analysis functions."""
    df = pd.DataFrame({
        "Invoice ID": [f"INV-{i}" for i in range(10)],
        "Branch": ["A", "B", "C", "A", "B", "C", "A", "B", "C", "A"],
        "City": ["Yangon", "Mandalay", "Naypyitaw"] * 3 + ["Yangon"],
        "Customer type": ["Member", "Normal"] * 5,
        "Gender": ["Female", "Male"] * 5,
        "Product line": [
            "Health and beauty", "Electronic accessories",
            "Home and lifestyle", "Food and beverages",
            "Sports and travel", "Fashion accessories",
            "Health and beauty", "Electronic accessories",
            "Home and lifestyle", "Food and beverages"
        ],
        "Unit price": [50.0, 30.0, 45.0, 60.0, 25.0, 35.0, 55.0, 40.0, 70.0, 20.0],
        "Quantity": [3, 5, 2, 4, 6, 1, 3, 7, 2, 8],
        "Tax 5%": [7.5, 7.5, 4.5, 12.0, 7.5, 1.75, 8.25, 14.0, 7.0, 8.0],
        "Total": [157.5, 157.5, 94.5, 252.0, 157.5, 36.75, 173.25, 294.0, 147.0, 168.0],
        "Date": pd.to_datetime([
            "2019-01-01", "2019-01-05", "2019-01-10", "2019-01-15",
            "2019-02-01", "2019-02-05", "2019-02-10", "2019-02-15",
            "2019-03-01", "2019-03-05"
        ]),
        "Payment": ["Cash", "Ewallet", "Credit card", "Cash", "Ewallet",
                     "Credit card", "Cash", "Ewallet", "Credit card", "Cash"],
        "cogs": [150.0, 150.0, 90.0, 240.0, 150.0, 35.0, 165.0, 280.0, 140.0, 160.0],
        "gross margin percentage": [4.761905] * 10,
        "gross income": [7.5, 7.5, 4.5, 12.0, 7.5, 1.75, 8.25, 14.0, 7.0, 8.0],
        "Rating": [7.0, 8.5, 6.0, 9.0, 7.5, 8.0, 6.5, 9.5, 7.0, 8.0],
        "Month": [1, 1, 1, 1, 2, 2, 2, 2, 3, 3],
        "Month_Name": ["January"] * 4 + ["February"] * 4 + ["March"] * 2,
        "Day_of_Week": ["Tuesday", "Saturday", "Thursday", "Tuesday",
                        "Friday", "Tuesday", "Sunday", "Friday", "Friday", "Tuesday"],
        "Hour": [10, 14, 9, 18, 11, 15, 13, 17, 10, 19],
    })
    return df


# ── Tests: compute_overall_metrics ────────────────────────

def test_overall_metrics_keys(sample_df):
    metrics = compute_overall_metrics(sample_df)
    assert "total_transactions" in metrics
    assert "total_sales" in metrics
    assert "average_transaction" in metrics
    assert "total_quantity" in metrics
    assert "avg_rating" in metrics


def test_overall_metrics_values(sample_df):
    metrics = compute_overall_metrics(sample_df)
    assert metrics["total_transactions"] == 10
    assert metrics["total_sales"] == round(sample_df["Total"].sum(), 2)
    assert metrics["total_quantity"] == int(sample_df["Quantity"].sum())


# ── Tests: sales_by_group ────────────────────────────────

def test_sales_by_group_sum(sample_df):
    result = sales_by_group(sample_df, "Branch", "Total", "sum")
    assert len(result) == 3
    assert "Total_sum" in result.columns
    # Sorted descending
    assert result.iloc[0]["Total_sum"] >= result.iloc[-1]["Total_sum"]


def test_sales_by_group_mean(sample_df):
    result = sales_by_group(sample_df, "Branch", "Total", "mean")
    assert "Total_mean" in result.columns


def test_sales_by_group_invalid_column(sample_df):
    with pytest.raises(ValueError, match="not found"):
        sales_by_group(sample_df, "NonExistent", "Total", "sum")


def test_sales_by_group_invalid_value_column(sample_df):
    with pytest.raises(ValueError, match="not found"):
        sales_by_group(sample_df, "Branch", "NonExistent", "sum")


# ── Tests: product_line_analysis ─────────────────────────

def test_product_line_analysis_keys(sample_df):
    results = product_line_analysis(sample_df)
    assert "sales_by_product" in results
    assert "txn_count_by_product" in results
    assert "avg_sale_by_product" in results
    assert "avg_rating_by_product" in results


def test_product_line_analysis_missing_column():
    df = pd.DataFrame({"A": [1, 2, 3]})
    results = product_line_analysis(df)
    assert "error" in results


# ── Tests: branch_analysis ───────────────────────────────

def test_branch_analysis_keys(sample_df):
    results = branch_analysis(sample_df)
    assert "sales_by_branch" in results
    assert "txn_count_by_branch" in results
    assert "avg_sale_by_branch" in results


def test_branch_analysis_missing_column():
    df = pd.DataFrame({"A": [1, 2, 3]})
    results = branch_analysis(df)
    assert "error" in results


# ── Tests: customer_analysis ─────────────────────────────

def test_customer_analysis(sample_df):
    results = customer_analysis(sample_df)
    assert "sales_by_customer_type" in results
    assert "sales_by_gender" in results
    assert "customer_gender_cross" in results


# ── Tests: payment_analysis ──────────────────────────────

def test_payment_analysis(sample_df):
    results = payment_analysis(sample_df)
    assert "sales_by_payment" in results
    assert "txn_by_payment" in results
    assert len(results["txn_by_payment"]) == 3


def test_payment_analysis_missing_column():
    df = pd.DataFrame({"A": [1, 2, 3]})
    results = payment_analysis(df)
    assert "error" in results


# ── Tests: time_analysis ─────────────────────────────────

def test_time_analysis_daily(sample_df):
    results = time_analysis(sample_df)
    assert "daily_sales" in results
    assert len(results["daily_sales"]) == 10  # each row has unique date


def test_time_analysis_monthly(sample_df):
    results = time_analysis(sample_df)
    assert "monthly_sales" in results
    assert len(results["monthly_sales"]) == 3  # Jan, Feb, Mar


def test_time_analysis_hourly(sample_df):
    results = time_analysis(sample_df)
    assert "hourly_sales" in results


# ── Tests: rating_analysis ───────────────────────────────

def test_rating_analysis(sample_df):
    results = rating_analysis(sample_df)
    assert "rating_stats" in results
    assert results["rating_stats"]["mean"] == round(sample_df["Rating"].mean(), 2)


def test_rating_analysis_missing_column():
    df = pd.DataFrame({"A": [1, 2, 3]})
    results = rating_analysis(df)
    assert "error" in results


# ── Tests: correlation_analysis ──────────────────────────

def test_correlation_analysis(sample_df):
    corr = correlation_analysis(sample_df)
    assert not corr.empty
    assert corr.shape[0] == corr.shape[1]
    # Diagonal should be 1.0
    for col in corr.columns:
        assert corr.loc[col, col] == 1.0


def test_correlation_analysis_insufficient_columns():
    df = pd.DataFrame({"A": [1, 2, 3]})
    corr = correlation_analysis(df)
    assert corr.empty


# ── Tests: generate_summary_table ────────────────────────

def test_generate_summary_table(sample_df):
    summary = generate_summary_table(sample_df)
    assert isinstance(summary, pd.DataFrame)
    assert "Metric" in summary.columns
    assert "Value" in summary.columns
    assert len(summary) > 0


# ── Tests: edge cases ────────────────────────────────────

def test_single_row_metrics():
    df = pd.DataFrame({
        "Total": [100.0],
        "Quantity": [5],
        "Rating": [7.0],
        "gross income": [5.0],
        "cogs": [95.0],
    })
    metrics = compute_overall_metrics(df)
    assert metrics["total_transactions"] == 1
    assert metrics["total_sales"] == 100.0
