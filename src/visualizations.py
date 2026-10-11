"""
Visualizations Module
=====================
Professional chart generation for the supermarket sales analysis project.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from typing import Optional

# ── Global Styling ──────────────────────────────────────────
STYLE_CONFIG = {
    "figure.figsize": (12, 6),
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.dpi": 150,
    "savefig.dpi": 200,
    "savefig.bbox": "tight",
    "font.family": "sans-serif",
}

# Professional color palette
PALETTE = [
    "#2E86AB", "#A23B72", "#F18F01", "#C73E1D", "#3B1F2B",
    "#44BBA4", "#E94F37", "#393E41", "#8E7DBE", "#3D5A80"
]

FIGURES_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "outputs", "figures"
)


def setup_style():
    """Apply the global matplotlib/seaborn style."""
    plt.rcParams.update(STYLE_CONFIG)
    sns.set_theme(style="whitegrid", palette=PALETTE)


def _save_figure(fig, filename: str, output_dir: Optional[str] = None):
    """Save figure to the outputs/figures directory."""
    if output_dir is None:
        output_dir = FIGURES_DIR
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    fig.savefig(filepath, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return filepath


def _format_currency(x, _):
    """Format axis labels as currency."""
    return f"${x:,.0f}"


# ─────────────────────────────────────────────────────────────
# 1. PRODUCT LINE CHARTS
# ─────────────────────────────────────────────────────────────

def plot_sales_by_product_line(df: pd.DataFrame, save: bool = True) -> plt.Figure:
    """Horizontal bar chart: Total sales by product line."""
    setup_style()
    data = df.groupby("Product line")["Total"].sum().sort_values()

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.barh(data.index, data.values, color=PALETTE[:len(data)], edgecolor="white", height=0.6)

    # Add value labels
    for bar in bars:
        width = bar.get_width()
        ax.text(width + data.max() * 0.01, bar.get_y() + bar.get_height() / 2,
                f'${width:,.0f}', ha='left', va='center', fontsize=10, fontweight='bold')

    ax.set_xlabel("Total Sales (USD)")
    ax.set_title("Total Sales by Product Line", fontsize=16, fontweight="bold", pad=15)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(_format_currency))
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()

    if save:
        _save_figure(fig, "sales_by_product_line.png")
    return fig


def plot_transaction_count_by_product(df: pd.DataFrame, save: bool = True) -> plt.Figure:
    """Bar chart: Transaction count by product line."""
    setup_style()
    data = df["Product line"].value_counts().sort_values()

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.barh(data.index, data.values, color=PALETTE[:len(data)], edgecolor="white", height=0.6)

    for bar in bars:
        width = bar.get_width()
        ax.text(width + 1, bar.get_y() + bar.get_height() / 2,
                f'{int(width)}', ha='left', va='center', fontsize=10, fontweight='bold')

    ax.set_xlabel("Number of Transactions")
    ax.set_title("Transaction Count by Product Line", fontsize=16, fontweight="bold", pad=15)
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()

    if save:
        _save_figure(fig, "txn_count_by_product_line.png")
    return fig


# ─────────────────────────────────────────────────────────────
# 2. BRANCH CHARTS
# ─────────────────────────────────────────────────────────────

def plot_sales_by_branch(df: pd.DataFrame, save: bool = True) -> plt.Figure:
    """Grouped bar chart: Sales and transaction count by branch."""
    setup_style()

    branch_sales = df.groupby("Branch")["Total"].sum()
    branch_count = df.groupby("Branch").size()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Sales
    bars1 = ax1.bar(branch_sales.index, branch_sales.values,
                    color=PALETTE[:3], edgecolor="white", width=0.5)
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2, height + branch_sales.max() * 0.01,
                 f'${height:,.0f}', ha='center', va='bottom', fontsize=11, fontweight='bold')

    ax1.set_title("Total Sales by Branch", fontsize=14, fontweight="bold")
    ax1.set_ylabel("Total Sales (USD)")
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(_format_currency))
    ax1.spines[["top", "right"]].set_visible(False)

    # Transaction count
    bars2 = ax2.bar(branch_count.index, branch_count.values,
                    color=PALETTE[:3], edgecolor="white", width=0.5)
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width() / 2, height + 1,
                 f'{int(height)}', ha='center', va='bottom', fontsize=11, fontweight='bold')

    ax2.set_title("Transaction Count by Branch", fontsize=14, fontweight="bold")
    ax2.set_ylabel("Number of Transactions")
    ax2.spines[["top", "right"]].set_visible(False)

    plt.suptitle("Branch Performance Comparison", fontsize=16, fontweight="bold", y=1.02)
    plt.tight_layout()

    if save:
        _save_figure(fig, "sales_by_branch.png")
    return fig


# ─────────────────────────────────────────────────────────────
# 3. CUSTOMER CHARTS
# ─────────────────────────────────────────────────────────────

def plot_customer_type_analysis(df: pd.DataFrame, save: bool = True) -> plt.Figure:
    """Bar charts: Sales by customer type and gender."""
    setup_style()
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Customer type
    if "Customer type" in df.columns:
        ct_sales = df.groupby("Customer type")["Total"].sum().sort_values(ascending=False)
        bars = axes[0].bar(ct_sales.index, ct_sales.values,
                           color=[PALETTE[0], PALETTE[1]], edgecolor="white", width=0.4)
        for bar in bars:
            height = bar.get_height()
            axes[0].text(bar.get_x() + bar.get_width() / 2, height + ct_sales.max() * 0.01,
                         f'${height:,.0f}', ha='center', va='bottom', fontsize=11, fontweight='bold')
        axes[0].set_title("Sales by Customer Type", fontsize=14, fontweight="bold")
        axes[0].set_ylabel("Total Sales (USD)")
        axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(_format_currency))
        axes[0].spines[["top", "right"]].set_visible(False)

    # Gender
    if "Gender" in df.columns:
        g_sales = df.groupby("Gender")["Total"].sum().sort_values(ascending=False)
        bars = axes[1].bar(g_sales.index, g_sales.values,
                           color=[PALETTE[2], PALETTE[3]], edgecolor="white", width=0.4)
        for bar in bars:
            height = bar.get_height()
            axes[1].text(bar.get_x() + bar.get_width() / 2, height + g_sales.max() * 0.01,
                         f'${height:,.0f}', ha='center', va='bottom', fontsize=11, fontweight='bold')
        axes[1].set_title("Sales by Gender", fontsize=14, fontweight="bold")
        axes[1].set_ylabel("Total Sales (USD)")
        axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(_format_currency))
        axes[1].spines[["top", "right"]].set_visible(False)

    plt.suptitle("Customer Segment Analysis", fontsize=16, fontweight="bold", y=1.02)
    plt.tight_layout()

    if save:
        _save_figure(fig, "customer_analysis.png")
    return fig


# ─────────────────────────────────────────────────────────────
# 4. PAYMENT CHARTS
# ─────────────────────────────────────────────────────────────

def plot_payment_analysis(df: pd.DataFrame, save: bool = True) -> plt.Figure:
    """Bar chart: Payment method distribution."""
    setup_style()

    if "Payment" not in df.columns:
        return None

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Sales by payment
    pay_sales = df.groupby("Payment")["Total"].sum().sort_values(ascending=False)
    bars = ax1.bar(pay_sales.index, pay_sales.values,
                   color=PALETTE[:3], edgecolor="white", width=0.5)
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2, height + pay_sales.max() * 0.01,
                 f'${height:,.0f}', ha='center', va='bottom', fontsize=11, fontweight='bold')
    ax1.set_title("Total Sales by Payment Method", fontsize=14, fontweight="bold")
    ax1.set_ylabel("Total Sales (USD)")
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(_format_currency))
    ax1.spines[["top", "right"]].set_visible(False)

    # Count by payment
    pay_count = df["Payment"].value_counts().sort_values(ascending=False)
    bars = ax2.bar(pay_count.index, pay_count.values,
                   color=PALETTE[:3], edgecolor="white", width=0.5)
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width() / 2, height + 1,
                 f'{int(height)}', ha='center', va='bottom', fontsize=11, fontweight='bold')
    ax2.set_title("Transactions by Payment Method", fontsize=14, fontweight="bold")
    ax2.set_ylabel("Number of Transactions")
    ax2.spines[["top", "right"]].set_visible(False)

    plt.suptitle("Payment Method Analysis", fontsize=16, fontweight="bold", y=1.02)
    plt.tight_layout()

    if save:
        _save_figure(fig, "payment_analysis.png")
    return fig


# ─────────────────────────────────────────────────────────────
# 5. TIME ANALYSIS CHARTS
# ─────────────────────────────────────────────────────────────

def plot_daily_sales_trend(df: pd.DataFrame, save: bool = True) -> plt.Figure:
    """Line chart: Daily sales trend."""
    setup_style()

    if "Date" not in df.columns:
        return None

    daily = df.groupby("Date")["Total"].sum().reset_index()
    daily = daily.sort_values("Date")

    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(daily["Date"], daily["Total"], color=PALETTE[0], linewidth=1.5, alpha=0.7)

    # Add rolling average
    if len(daily) > 7:
        daily["MA_7"] = daily["Total"].rolling(window=7, center=True).mean()
        ax.plot(daily["Date"], daily["MA_7"], color=PALETTE[1],
                linewidth=2.5, label="7-day Moving Average")
        ax.legend()

    ax.set_title("Daily Sales Trend", fontsize=16, fontweight="bold", pad=15)
    ax.set_xlabel("Date")
    ax.set_ylabel("Daily Sales (USD)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(_format_currency))
    ax.spines[["top", "right"]].set_visible(False)
    plt.xticks(rotation=45)
    plt.tight_layout()

    if save:
        _save_figure(fig, "daily_sales_trend.png")
    return fig


def plot_hourly_sales(df: pd.DataFrame, save: bool = True) -> plt.Figure:
    """Bar chart: Sales distribution by hour of day."""
    setup_style()

    if "Hour" not in df.columns:
        return None

    hourly = df.groupby("Hour")["Total"].agg(["sum", "count"]).reset_index()
    hourly.columns = ["Hour", "Total_Sales", "Txn_Count"]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

    # Total sales by hour
    ax1.bar(hourly["Hour"], hourly["Total_Sales"],
            color=PALETTE[0], edgecolor="white", alpha=0.85)
    ax1.set_title("Total Sales by Hour of Day", fontsize=14, fontweight="bold")
    ax1.set_ylabel("Total Sales (USD)")
    ax1.set_xlabel("Hour")
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(_format_currency))
    ax1.set_xticks(hourly["Hour"])
    ax1.spines[["top", "right"]].set_visible(False)

    # Transaction count by hour
    ax2.bar(hourly["Hour"], hourly["Txn_Count"],
            color=PALETTE[1], edgecolor="white", alpha=0.85)
    ax2.set_title("Transaction Count by Hour of Day", fontsize=14, fontweight="bold")
    ax2.set_ylabel("Number of Transactions")
    ax2.set_xlabel("Hour")
    ax2.set_xticks(hourly["Hour"])
    ax2.spines[["top", "right"]].set_visible(False)

    plt.tight_layout()

    if save:
        _save_figure(fig, "hourly_sales.png")
    return fig


def plot_day_of_week_sales(df: pd.DataFrame, save: bool = True) -> plt.Figure:
    """Bar chart: Sales by day of week."""
    setup_style()

    if "Day_of_Week" not in df.columns:
        return None

    dow_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    dow = df.groupby("Day_of_Week")["Total"].sum().reindex(dow_order)

    fig, ax = plt.subplots(figsize=(12, 6))
    colors = [PALETTE[4] if d in ["Saturday", "Sunday"] else PALETTE[0] for d in dow.index]
    bars = ax.bar(dow.index, dow.values, color=colors, edgecolor="white", width=0.6)

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + dow.max() * 0.01,
                f'${height:,.0f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

    ax.set_title("Total Sales by Day of Week", fontsize=16, fontweight="bold", pad=15)
    ax.set_ylabel("Total Sales (USD)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(_format_currency))
    ax.spines[["top", "right"]].set_visible(False)
    plt.xticks(rotation=30)
    plt.tight_layout()

    if save:
        _save_figure(fig, "day_of_week_sales.png")
    return fig


def plot_monthly_sales(df: pd.DataFrame, save: bool = True) -> plt.Figure:
    """Bar chart: Monthly sales."""
    setup_style()

    if "Month_Name" not in df.columns or "Month" not in df.columns:
        return None

    monthly = df.groupby(["Month", "Month_Name"])["Total"].sum().reset_index()
    monthly = monthly.sort_values("Month")

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(monthly["Month_Name"], monthly["Total"],
                  color=PALETTE[:len(monthly)], edgecolor="white", width=0.5)

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + monthly["Total"].max() * 0.01,
                f'${height:,.0f}', ha='center', va='bottom', fontsize=11, fontweight='bold')

    ax.set_title("Monthly Sales Performance", fontsize=16, fontweight="bold", pad=15)
    ax.set_ylabel("Total Sales (USD)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(_format_currency))
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()

    if save:
        _save_figure(fig, "monthly_sales.png")
    return fig


# ─────────────────────────────────────────────────────────────
# 6. RATING CHARTS
# ─────────────────────────────────────────────────────────────

def plot_rating_distribution(df: pd.DataFrame, save: bool = True) -> plt.Figure:
    """Histogram: Rating distribution."""
    setup_style()

    if "Rating" not in df.columns:
        return None

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(df["Rating"], bins=20, color=PALETTE[0], edgecolor="white", alpha=0.85)
    ax.axvline(df["Rating"].mean(), color=PALETTE[1], linestyle="--",
               linewidth=2, label=f'Mean: {df["Rating"].mean():.2f}')
    ax.axvline(df["Rating"].median(), color=PALETTE[2], linestyle="--",
               linewidth=2, label=f'Median: {df["Rating"].median():.2f}')

    ax.set_title("Customer Rating Distribution", fontsize=16, fontweight="bold", pad=15)
    ax.set_xlabel("Rating")
    ax.set_ylabel("Frequency")
    ax.legend(fontsize=11)
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()

    if save:
        _save_figure(fig, "rating_distribution.png")
    return fig


def plot_rating_by_product_line(df: pd.DataFrame, save: bool = True) -> plt.Figure:
    """Box plot: Rating by product line."""
    setup_style()

    if "Rating" not in df.columns or "Product line" not in df.columns:
        return None

    fig, ax = plt.subplots(figsize=(12, 6))
    order = df.groupby("Product line")["Rating"].mean().sort_values(ascending=False).index
    sns.boxplot(data=df, x="Product line", y="Rating", order=order,
                palette=PALETTE[:6], ax=ax, width=0.5)

    ax.set_title("Customer Rating by Product Line", fontsize=16, fontweight="bold", pad=15)
    ax.set_xlabel("Product Line")
    ax.set_ylabel("Rating")
    ax.spines[["top", "right"]].set_visible(False)
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    if save:
        _save_figure(fig, "rating_by_product_line.png")
    return fig


# ─────────────────────────────────────────────────────────────
# 7. CORRELATION HEATMAP
# ─────────────────────────────────────────────────────────────

def plot_correlation_heatmap(df: pd.DataFrame, save: bool = True) -> plt.Figure:
    """Heatmap: Correlation between numerical variables."""
    setup_style()

    numeric_cols = ["Unit price", "Quantity", "Tax 5%", "Total", "cogs",
                    "gross income", "Rating"]
    available = [c for c in numeric_cols if c in df.columns]

    if len(available) < 2:
        return None

    corr = df[available].corr()

    fig, ax = plt.subplots(figsize=(10, 8))
    mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
    sns.heatmap(corr, mask=mask, annot=True, fmt=".2f",
                cmap="RdBu_r", center=0, square=True,
                linewidths=1, linecolor="white",
                ax=ax, vmin=-1, vmax=1,
                cbar_kws={"shrink": 0.8, "label": "Correlation"})

    ax.set_title("Correlation Heatmap of Numerical Variables",
                 fontsize=16, fontweight="bold", pad=15)
    plt.tight_layout()

    if save:
        _save_figure(fig, "correlation_heatmap.png")
    return fig


# ─────────────────────────────────────────────────────────────
# 8. DISTRIBUTION CHARTS
# ─────────────────────────────────────────────────────────────

def plot_sales_distribution(df: pd.DataFrame, save: bool = True) -> plt.Figure:
    """Histogram: Distribution of transaction totals."""
    setup_style()

    if "Total" not in df.columns:
        return None

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.hist(df["Total"], bins=30, color=PALETTE[0], edgecolor="white", alpha=0.85)
    ax.axvline(df["Total"].mean(), color=PALETTE[1], linestyle="--",
               linewidth=2, label=f'Mean: ${df["Total"].mean():,.2f}')
    ax.axvline(df["Total"].median(), color=PALETTE[2], linestyle="--",
               linewidth=2, label=f'Median: ${df["Total"].median():,.2f}')

    ax.set_title("Distribution of Transaction Values", fontsize=16, fontweight="bold", pad=15)
    ax.set_xlabel("Transaction Total (USD)")
    ax.set_ylabel("Frequency")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(_format_currency))
    ax.legend(fontsize=11)
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()

    if save:
        _save_figure(fig, "sales_distribution.png")
    return fig


# ─────────────────────────────────────────────────────────────
# 9. MASTER CHART GENERATOR
# ─────────────────────────────────────────────────────────────

def generate_all_charts(df: pd.DataFrame, output_dir: Optional[str] = None) -> list:
    """
    Generate all available visualizations.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataset.
    output_dir : str, optional
        Directory to save figures. Defaults to outputs/figures/.

    Returns
    -------
    list
        List of generated chart filenames.
    """
    if output_dir:
        global FIGURES_DIR
        FIGURES_DIR = output_dir
        os.makedirs(output_dir, exist_ok=True)

    generated = []

    chart_functions = [
        ("sales_by_product_line.png", plot_sales_by_product_line),
        ("txn_count_by_product_line.png", plot_transaction_count_by_product),
        ("sales_by_branch.png", plot_sales_by_branch),
        ("customer_analysis.png", plot_customer_type_analysis),
        ("payment_analysis.png", plot_payment_analysis),
        ("daily_sales_trend.png", plot_daily_sales_trend),
        ("hourly_sales.png", plot_hourly_sales),
        ("day_of_week_sales.png", plot_day_of_week_sales),
        ("monthly_sales.png", plot_monthly_sales),
        ("rating_distribution.png", plot_rating_distribution),
        ("rating_by_product_line.png", plot_rating_by_product_line),
        ("correlation_heatmap.png", plot_correlation_heatmap),
        ("sales_distribution.png", plot_sales_distribution),
    ]

    for filename, func in chart_functions:
        try:
            fig = func(df, save=True)
            if fig is not None:
                generated.append(filename)
        except Exception as e:
            print(f"Warning: Could not generate {filename}: {e}")

    return generated
