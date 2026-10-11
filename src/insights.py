"""
Insights Module
===============
Generates evidence-based business insights from the analysis results.
"""

import pandas as pd
import numpy as np
from typing import Optional
from src.analysis import (
    compute_overall_metrics, product_line_analysis, branch_analysis,
    customer_analysis, payment_analysis, time_analysis, rating_analysis
)


def generate_insights(df: pd.DataFrame) -> list:
    """
    Generate a list of evidence-based business insights from the dataset.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataset.

    Returns
    -------
    list of dict
        Each dict has keys: 'category', 'finding', 'metric', 'recommendation', 'limitation'.
    """
    insights = []
    metrics = compute_overall_metrics(df)

    # ── Overall Performance ────────────────────────────
    insights.append({
        "category": "Overall Performance",
        "finding": (
            f"The dataset contains {metrics['total_transactions']:,} transactions "
            f"with total recorded sales of ${metrics.get('total_sales', 0):,.2f}."
        ),
        "metric": (
            f"Average transaction value: ${metrics.get('average_transaction', 0):,.2f}, "
            f"Median: ${metrics.get('median_transaction', 0):,.2f}"
        ),
        "recommendation": (
            "Use the average transaction value as a baseline for setting promotional "
            "thresholds (e.g., 'spend $X more to unlock a reward')."
        ),
        "limitation": (
            "The dataset covers a limited time window. Overall performance metrics "
            "may not represent long-term trends."
        )
    })

    # ── Product Line Insights ──────────────────────────
    if "Product line" in df.columns:
        pl_results = product_line_analysis(df)
        if "sales_by_product" in pl_results:
            top = pl_results["sales_by_product"].iloc[0]
            bottom = pl_results["sales_by_product"].iloc[-1]
            insights.append({
                "category": "Product Performance",
                "finding": (
                    f"'{top['Product line']}' is the top-selling product line with "
                    f"${top['Total_sum']:,.2f} in total sales, while "
                    f"'{bottom['Product line']}' has the lowest sales at "
                    f"${bottom['Total_sum']:,.2f}."
                ),
                "metric": (
                    f"Top: ${top['Total_sum']:,.2f} | Bottom: ${bottom['Total_sum']:,.2f} | "
                    f"Difference: ${top['Total_sum'] - bottom['Total_sum']:,.2f}"
                ),
                "recommendation": (
                    f"Investigate why '{bottom['Product line']}' underperforms. "
                    f"Consider targeted promotions or better shelf placement. "
                    f"Capitalize on '{top['Product line']}' momentum with premium or "
                    f"bundled offerings."
                ),
                "limitation": (
                    "Sales differences could reflect product availability, pricing, or "
                    "seasonal demand rather than intrinsic popularity."
                )
            })

    # ── Branch Insights ────────────────────────────────
    if "Branch" in df.columns:
        br_results = branch_analysis(df)
        if "sales_by_branch" in br_results:
            top_br = br_results["sales_by_branch"].iloc[0]
            bot_br = br_results["sales_by_branch"].iloc[-1]
            insights.append({
                "category": "Branch Performance",
                "finding": (
                    f"Branch {top_br['Branch']} leads in total sales "
                    f"(${top_br['Total_sum']:,.2f}), while Branch {bot_br['Branch']} "
                    f"has the lowest (${bot_br['Total_sum']:,.2f})."
                ),
                "metric": f"Sales gap: ${top_br['Total_sum'] - bot_br['Total_sum']:,.2f}",
                "recommendation": (
                    f"Examine the operational factors at Branch {top_br['Branch']} that "
                    f"contribute to its success. Apply best practices to other branches. "
                    f"Conduct a localized assessment at Branch {bot_br['Branch']} for improvement."
                ),
                "limitation": (
                    "Branch differences may be influenced by location demographics, "
                    "store size, and local competition."
                )
            })

    # ── Customer Insights ──────────────────────────────
    if "Customer type" in df.columns:
        ct_results = customer_analysis(df)
        if "sales_by_customer_type" in ct_results:
            ct_data = ct_results["sales_by_customer_type"]
            member_row = ct_data[ct_data["Customer type"] == "Member"]
            normal_row = ct_data[ct_data["Customer type"] == "Normal"]
            if len(member_row) > 0 and len(normal_row) > 0:
                m_sales = member_row.iloc[0]["Total_sum"]
                n_sales = normal_row.iloc[0]["Total_sum"]
                insights.append({
                    "category": "Customer Segments",
                    "finding": (
                        f"Member customers account for ${m_sales:,.2f} in sales vs "
                        f"Normal customers at ${n_sales:,.2f}."
                    ),
                    "metric": f"Member: ${m_sales:,.2f} | Normal: ${n_sales:,.2f}",
                    "recommendation": (
                        "Strengthen the membership program by offering exclusive discounts "
                        "or early access to promotions. Incentivize Normal customers to "
                        "become Members."
                    ),
                    "limitation": (
                        "The 'Member' vs 'Normal' split is based on the dataset labels. "
                        "Actual loyalty program details are unknown."
                    )
                })

    # ── Payment Insights ───────────────────────────────
    if "Payment" in df.columns:
        pay_results = payment_analysis(df)
        if "txn_by_payment" in pay_results:
            pay_data = pay_results["txn_by_payment"]
            top_pay = pay_data.sort_values("Transaction_Count", ascending=False).iloc[0]
            insights.append({
                "category": "Payment Methods",
                "finding": (
                    f"'{top_pay['Payment']}' is the most frequently used payment method "
                    f"with {top_pay['Transaction_Count']} transactions."
                ),
                "metric": f"Top method: {top_pay['Payment']} ({top_pay['Transaction_Count']} txns)",
                "recommendation": (
                    "Ensure seamless checkout for all payment methods. Consider partnerships "
                    "with e-wallet providers for loyalty promotions."
                ),
                "limitation": (
                    "Payment preferences may be influenced by demographics, promotions, "
                    "or infrastructure availability."
                )
            })

    # ── Time Insights ──────────────────────────────────
    if "Hour" in df.columns:
        hourly = df.groupby("Hour")["Total"].sum()
        peak_hour = hourly.idxmax()
        peak_sales = hourly.max()
        insights.append({
            "category": "Peak Hours",
            "finding": (
                f"The peak sales hour is {int(peak_hour)}:00 with "
                f"${peak_sales:,.2f} in total sales."
            ),
            "metric": f"Peak: {int(peak_hour)}:00 (${peak_sales:,.2f})",
            "recommendation": (
                f"Ensure adequate staffing during peak hour ({int(peak_hour)}:00). "
                f"Schedule restocking and promotional activities to align with "
                f"high-traffic periods."
            ),
            "limitation": "Hourly patterns may vary by branch, day of week, and season."
        })

    # ── Rating Insights ────────────────────────────────
    if "Rating" in df.columns:
        avg_rating = df["Rating"].mean()
        insights.append({
            "category": "Customer Satisfaction",
            "finding": (
                f"The average customer rating is {avg_rating:.2f} out of 10. "
                f"Ratings range from {df['Rating'].min():.1f} to {df['Rating'].max():.1f}."
            ),
            "metric": f"Mean: {avg_rating:.2f}, Median: {df['Rating'].median():.2f}",
            "recommendation": (
                "Investigate factors behind lower ratings. Conduct customer feedback "
                "surveys and implement targeted improvements to boost satisfaction."
            ),
            "limitation": (
                "Ratings may reflect immediate post-purchase sentiment and may not "
                "capture long-term satisfaction or repeat purchase intent."
            )
        })

    return insights


def format_insights_text(insights: list) -> str:
    """
    Format insights list into a readable text block.

    Parameters
    ----------
    insights : list of dict
        Insights from generate_insights().

    Returns
    -------
    str
        Formatted text.
    """
    lines = []
    lines.append("=" * 70)
    lines.append("BUSINESS INSIGHTS AND RECOMMENDATIONS")
    lines.append("=" * 70)

    for i, insight in enumerate(insights, 1):
        lines.append(f"\n{'─' * 60}")
        lines.append(f"Insight {i}: {insight['category']}")
        lines.append(f"{'─' * 60}")
        lines.append(f"\n📊 Finding:\n   {insight['finding']}")
        lines.append(f"\n📈 Key Metric:\n   {insight['metric']}")
        lines.append(f"\n💡 Recommendation:\n   {insight['recommendation']}")
        lines.append(f"\n⚠️  Limitation:\n   {insight['limitation']}")

    lines.append(f"\n{'=' * 70}")
    return "\n".join(lines)


def insights_to_dataframe(insights: list) -> pd.DataFrame:
    """
    Convert insights list to a DataFrame for export.

    Parameters
    ----------
    insights : list of dict
        Insights from generate_insights().

    Returns
    -------
    pd.DataFrame
        Tabular format of insights.
    """
    return pd.DataFrame(insights)
