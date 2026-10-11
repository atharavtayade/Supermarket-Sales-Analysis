"""
Analysis Module
===============
Contains analytical functions for computing summary statistics, KPIs,
and group-level analyses on the supermarket sales dataset.
"""

import pandas as pd
import numpy as np
from typing import Optional


def compute_overall_metrics(df: pd.DataFrame) -> dict:
    """
    Compute overall sales performance metrics.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataset.

    Returns
    -------
    dict
        Dictionary of key performance indicators.
    """
    metrics = {}

    metrics["total_transactions"] = len(df)

    if "Total" in df.columns:
        metrics["total_sales"] = round(df["Total"].sum(), 2)
        metrics["average_transaction"] = round(df["Total"].mean(), 2)
        metrics["median_transaction"] = round(df["Total"].median(), 2)
        metrics["max_transaction"] = round(df["Total"].max(), 2)
        metrics["min_transaction"] = round(df["Total"].min(), 2)
        metrics["std_transaction"] = round(df["Total"].std(), 2)

    if "Quantity" in df.columns:
        metrics["total_quantity"] = int(df["Quantity"].sum())
        metrics["avg_quantity_per_txn"] = round(df["Quantity"].mean(), 2)

    if "gross income" in df.columns:
        metrics["total_gross_income"] = round(df["gross income"].sum(), 2)
        metrics["avg_gross_income"] = round(df["gross income"].mean(), 2)

    if "Rating" in df.columns:
        metrics["avg_rating"] = round(df["Rating"].mean(), 2)
        metrics["median_rating"] = round(df["Rating"].median(), 2)

    if "cogs" in df.columns:
        metrics["total_cogs"] = round(df["cogs"].sum(), 2)

    return metrics


def sales_by_group(df: pd.DataFrame, group_col: str,
                   value_col: str = "Total",
                   agg_func: str = "sum") -> pd.DataFrame:
    """
    Aggregate sales by a categorical group column.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataset.
    group_col : str
        Column to group by.
    value_col : str
        Column to aggregate (default: 'Total').
    agg_func : str
        Aggregation function ('sum', 'mean', 'count', 'median').

    Returns
    -------
    pd.DataFrame
        Grouped and sorted results.
    """
    if group_col not in df.columns:
        raise ValueError(f"Column '{group_col}' not found in dataset.")
    if value_col not in df.columns:
        raise ValueError(f"Column '{value_col}' not found in dataset.")

    result = df.groupby(group_col)[value_col].agg(agg_func).reset_index()
    result.columns = [group_col, f"{value_col}_{agg_func}"]
    result = result.sort_values(f"{value_col}_{agg_func}", ascending=False).reset_index(drop=True)

    return result


def product_line_analysis(df: pd.DataFrame) -> dict:
    """
    Comprehensive product line analysis.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataset with 'Product line' column.

    Returns
    -------
    dict
        Product line analysis results.
    """
    if "Product line" not in df.columns:
        return {"error": "Product line column not found"}

    results = {}

    # Total sales by product line
    results["sales_by_product"] = sales_by_group(df, "Product line", "Total", "sum")

    # Transaction count by product line
    results["txn_count_by_product"] = df.groupby("Product line").size().reset_index(name="Transaction_Count")
    results["txn_count_by_product"] = results["txn_count_by_product"].sort_values(
        "Transaction_Count", ascending=False
    ).reset_index(drop=True)

    # Average transaction by product line
    results["avg_sale_by_product"] = sales_by_group(df, "Product line", "Total", "mean")

    # Average rating by product line
    if "Rating" in df.columns:
        results["avg_rating_by_product"] = sales_by_group(df, "Product line", "Rating", "mean")

    # Average quantity by product line
    if "Quantity" in df.columns:
        results["avg_qty_by_product"] = sales_by_group(df, "Product line", "Quantity", "mean")

    return results


def branch_analysis(df: pd.DataFrame) -> dict:
    """
    Branch-level performance analysis.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataset with 'Branch' column.

    Returns
    -------
    dict
        Branch analysis results.
    """
    if "Branch" not in df.columns:
        return {"error": "Branch column not found"}

    results = {}

    results["sales_by_branch"] = sales_by_group(df, "Branch", "Total", "sum")
    results["txn_count_by_branch"] = df.groupby("Branch").size().reset_index(name="Transaction_Count")
    results["avg_sale_by_branch"] = sales_by_group(df, "Branch", "Total", "mean")

    if "Rating" in df.columns:
        results["avg_rating_by_branch"] = sales_by_group(df, "Branch", "Rating", "mean")

    if "gross income" in df.columns:
        results["gross_income_by_branch"] = sales_by_group(df, "Branch", "gross income", "sum")

    # Branch-City mapping
    if "City" in df.columns:
        results["branch_city_map"] = df.groupby("Branch")["City"].first().reset_index()

    return results


def customer_analysis(df: pd.DataFrame) -> dict:
    """
    Customer-type and gender analysis.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataset.

    Returns
    -------
    dict
        Customer analysis results.
    """
    results = {}

    if "Customer type" in df.columns:
        results["sales_by_customer_type"] = sales_by_group(df, "Customer type", "Total", "sum")
        results["txn_by_customer_type"] = df.groupby("Customer type").size().reset_index(name="Transaction_Count")
        results["avg_sale_by_customer_type"] = sales_by_group(df, "Customer type", "Total", "mean")

    if "Gender" in df.columns:
        results["sales_by_gender"] = sales_by_group(df, "Gender", "Total", "sum")
        results["txn_by_gender"] = df.groupby("Gender").size().reset_index(name="Transaction_Count")

    # Cross analysis: Customer type × Gender
    if "Customer type" in df.columns and "Gender" in df.columns:
        cross = df.groupby(["Customer type", "Gender"])["Total"].agg(["sum", "mean", "count"]).reset_index()
        cross.columns = ["Customer type", "Gender", "Total_Sales", "Avg_Sale", "Txn_Count"]
        results["customer_gender_cross"] = cross

    return results


def payment_analysis(df: pd.DataFrame) -> dict:
    """
    Payment method analysis.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataset with 'Payment' column.

    Returns
    -------
    dict
        Payment analysis results.
    """
    if "Payment" not in df.columns:
        return {"error": "Payment column not found"}

    results = {}

    results["sales_by_payment"] = sales_by_group(df, "Payment", "Total", "sum")
    results["txn_by_payment"] = df.groupby("Payment").size().reset_index(name="Transaction_Count")
    results["avg_sale_by_payment"] = sales_by_group(df, "Payment", "Total", "mean")

    return results


def time_analysis(df: pd.DataFrame) -> dict:
    """
    Temporal analysis of sales trends.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataset with 'Date' and optional 'Hour' columns.

    Returns
    -------
    dict
        Time-based analysis results.
    """
    results = {}

    if "Date" in df.columns:
        # Daily sales
        daily = df.groupby("Date")["Total"].sum().reset_index()
        daily.columns = ["Date", "Daily_Sales"]
        daily = daily.sort_values("Date")
        results["daily_sales"] = daily

        # Monthly sales
        if "Month_Name" in df.columns and "Month" in df.columns:
            monthly = df.groupby(["Month", "Month_Name"])["Total"].agg(
                ["sum", "mean", "count"]
            ).reset_index()
            monthly.columns = ["Month", "Month_Name", "Total_Sales", "Avg_Sale", "Txn_Count"]
            monthly = monthly.sort_values("Month")
            results["monthly_sales"] = monthly

        # Day of week sales
        if "Day_of_Week" in df.columns:
            dow_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            dow = df.groupby("Day_of_Week")["Total"].agg(["sum", "mean", "count"]).reset_index()
            dow.columns = ["Day_of_Week", "Total_Sales", "Avg_Sale", "Txn_Count"]
            dow["Day_of_Week"] = pd.Categorical(dow["Day_of_Week"], categories=dow_order, ordered=True)
            dow = dow.sort_values("Day_of_Week")
            results["day_of_week_sales"] = dow

    # Hourly analysis
    if "Hour" in df.columns:
        hourly = df.groupby("Hour")["Total"].agg(["sum", "mean", "count"]).reset_index()
        hourly.columns = ["Hour", "Total_Sales", "Avg_Sale", "Txn_Count"]
        hourly = hourly.sort_values("Hour")
        results["hourly_sales"] = hourly

    return results


def rating_analysis(df: pd.DataFrame) -> dict:
    """
    Customer rating analysis.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataset with 'Rating' column.

    Returns
    -------
    dict
        Rating analysis results.
    """
    if "Rating" not in df.columns:
        return {"error": "Rating column not found"}

    results = {}

    results["rating_stats"] = {
        "mean": round(df["Rating"].mean(), 2),
        "median": round(df["Rating"].median(), 2),
        "std": round(df["Rating"].std(), 2),
        "min": round(df["Rating"].min(), 2),
        "max": round(df["Rating"].max(), 2),
    }

    # Rating by various groups
    for col in ["Branch", "Product line", "Customer type", "Gender"]:
        if col in df.columns:
            group_rating = df.groupby(col)["Rating"].agg(["mean", "median", "std"]).reset_index()
            group_rating.columns = [col, "Mean_Rating", "Median_Rating", "Std_Rating"]
            group_rating = group_rating.round(2)
            results[f"rating_by_{col.lower().replace(' ', '_')}"] = group_rating

    return results


def correlation_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute correlation matrix for numerical columns.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataset.

    Returns
    -------
    pd.DataFrame
        Correlation matrix.
    """
    numeric_cols = ["Unit price", "Quantity", "Tax 5%", "Total", "cogs",
                    "gross income", "Rating"]
    available_cols = [c for c in numeric_cols if c in df.columns]

    if len(available_cols) < 2:
        return pd.DataFrame()

    return df[available_cols].corr().round(3)


def generate_summary_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate a comprehensive summary metrics table.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataset.

    Returns
    -------
    pd.DataFrame
        Summary table with metric names and values.
    """
    metrics = compute_overall_metrics(df)
    summary = pd.DataFrame(
        list(metrics.items()),
        columns=["Metric", "Value"]
    )
    return summary
