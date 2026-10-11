"""
Generate the Professional Word Report (DOCX)
=============================================
This script generates AtharavTayade_ProjectReport.docx from the executed analysis.
"""

import os
import sys
import pandas as pd
import numpy as np

# Ensure UTF-8 output encoding on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.abspath('.'))

from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_ORIENT

from src.data_loader import load_dataset, inspect_dataset, validate_schema
from src.data_cleaning import clean_dataset
from src.analysis import (
    compute_overall_metrics, product_line_analysis, branch_analysis,
    customer_analysis, payment_analysis, time_analysis,
    rating_analysis, correlation_analysis
)
from src.insights import generate_insights


def add_styled_paragraph(doc, text, style='Normal', bold=False, size=11,
                         alignment=WD_ALIGN_PARAGRAPH.LEFT, space_after=6):
    """Add a paragraph with custom formatting."""
    para = doc.add_paragraph()
    para.alignment = alignment
    para.paragraph_format.space_after = Pt(space_after)
    run = para.add_run(text)
    run.bold = bold
    run.font.size = Pt(size)
    return para


def add_table_from_df(doc, df, caption=None):
    """Add a formatted table from a DataFrame."""
    if caption:
        p = doc.add_paragraph()
        run = p.add_run(caption)
        run.bold = True
        run.font.size = Pt(10)

    table = doc.add_table(rows=1 + len(df), cols=len(df.columns))
    table.style = 'Light Grid Accent 1'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    # Header
    for j, col in enumerate(df.columns):
        cell = table.rows[0].cells[j]
        cell.text = str(col)
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.bold = True
                run.font.size = Pt(9)

    # Data rows
    for i, row in df.iterrows():
        for j, val in enumerate(row):
            cell = table.rows[i + 1].cells[j]
            if isinstance(val, float):
                cell.text = f"{val:,.2f}"
            else:
                cell.text = str(val)
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.size = Pt(9)

    doc.add_paragraph()  # spacing


def add_figure(doc, filepath, caption, width=5.5):
    """Add a figure with caption."""
    if os.path.exists(filepath):
        doc.add_picture(filepath, width=Inches(width))
        last_paragraph = doc.paragraphs[-1]
        last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

        cap = doc.add_paragraph()
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = cap.add_run(caption)
        run.italic = True
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor(100, 100, 100)


def generate_report():
    """Generate the complete Word report."""
    print("Generating Word report...")

    # Load and process data
    DATA_PATH = os.path.join('data', 'supermarket_sales.csv')
    df_raw = load_dataset(DATA_PATH)
    df, cleaning_report = clean_dataset(df_raw)
    metrics = compute_overall_metrics(df)
    pl_results = product_line_analysis(df)
    br_results = branch_analysis(df)
    cust_results = customer_analysis(df)
    pay_results = payment_analysis(df)
    time_results = time_analysis(df)
    rate_results = rating_analysis(df)
    insights = generate_insights(df)

    FIGURES = os.path.join('outputs', 'figures')

    # Create document
    doc = Document()

    # Set default font
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Calibri'
    font.size = Pt(11)

    # ── TITLE PAGE ──────────────────────────────────────────
    for _ in range(4):
        doc.add_paragraph()

    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run('Supermarket Sales Analysis')
    run.bold = True
    run.font.size = Pt(28)
    run.font.color.rgb = RGBColor(0, 51, 102)

    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = subtitle.add_run('Data Analytics with AI — Internship Project Report')
    run.font.size = Pt(16)
    run.font.color.rgb = RGBColor(80, 80, 80)

    doc.add_paragraph()

    details = [
        ('Student', 'Atharav Tayade'),
        ('Program', 'AICTE | IBM SkillsBuild Data Analytics with AI Internship 2026'),
        ('Organization', 'BharatCares'),
        ('Domain', 'Data Analytics with AI'),
        ('Date', 'October 2026'),
    ]

    for label, value in details:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(f'{label}: ')
        run.bold = True
        run.font.size = Pt(12)
        run = p.add_run(value)
        run.font.size = Pt(12)

    doc.add_page_break()

    # ── TABLE OF CONTENTS (placeholder) ────────────────────
    doc.add_heading('Table of Contents', level=1)
    toc_items = [
        '1. Abstract',
        '2. Introduction',
        '3. Problem Statement',
        '4. Objectives',
        '5. Dataset Description',
        '6. Tools and Technologies',
        '7. Methodology',
        '8. Data Cleaning and Preprocessing',
        '9. Exploratory Data Analysis',
        '10. Machine Learning Model',
        '11. Results and Findings',
        '12. Business Recommendations',
        '13. Limitations',
        '14. Conclusion',
        '15. References',
    ]
    for item in toc_items:
        doc.add_paragraph(item, style='List Number')

    doc.add_page_break()

    # ── 1. ABSTRACT ─────────────────────────────────────────
    doc.add_heading('1. Abstract', level=1)
    doc.add_paragraph(
        f"This report presents a comprehensive data analytics study of supermarket sales "
        f"transactions. The dataset comprises {metrics['total_transactions']:,} transactions "
        f"from three supermarket branches, totaling ${metrics.get('total_sales', 0):,.2f} in "
        f"recorded sales. The analysis covers product line performance, branch comparisons, "
        f"customer segmentation, payment method preferences, temporal trends, and customer "
        f"satisfaction ratings. A Random Forest regression model was developed for sales "
        f"prediction as a demonstration of the machine learning pipeline. Key findings reveal "
        f"performance variations across product categories and branches, with actionable "
        f"recommendations for revenue optimization and customer experience improvement."
    )

    # ── 2. INTRODUCTION ─────────────────────────────────────
    doc.add_heading('2. Introduction', level=1)
    doc.add_paragraph(
        "The retail industry generates vast amounts of transactional data that, when analyzed "
        "systematically, can reveal actionable insights for business optimization. This project "
        "applies data analytics techniques to a supermarket sales dataset as part of the "
        "AICTE | IBM SkillsBuild Data Analytics with AI Internship program conducted through "
        "BharatCares. The study demonstrates a complete data analytics workflow from data "
        "loading and cleaning through exploratory analysis, visualization, machine learning, "
        "and insight generation."
    )

    # ── 3. PROBLEM STATEMENT ────────────────────────────────
    doc.add_heading('3. Problem Statement', level=1)
    doc.add_paragraph(
        "The supermarket management requires data-driven answers to the following questions:"
    )
    problems = [
        "Which product lines generate the most revenue and transactions?",
        "How do the three branches compare in sales performance?",
        "What are the purchasing patterns of Member vs Normal customers?",
        "Which payment methods are preferred, and do they affect transaction values?",
        "What are the peak sales periods (hourly, daily, monthly)?",
        "How satisfied are customers, and does satisfaction vary across segments?",
        "Can transaction totals be predicted from purchase characteristics?"
    ]
    for p in problems:
        doc.add_paragraph(p, style='List Bullet')

    # ── 4. OBJECTIVES ───────────────────────────────────────
    doc.add_heading('4. Objectives', level=1)
    objectives = [
        "Load, inspect, and validate the supermarket sales dataset",
        "Clean and preprocess data for reliable analysis",
        "Conduct exploratory data analysis across multiple business dimensions",
        "Create professional visualizations to communicate findings",
        "Build and evaluate a machine learning model for sales prediction",
        "Generate evidence-based business insights and recommendations"
    ]
    for o in objectives:
        doc.add_paragraph(o, style='List Bullet')

    # ── 5. DATASET DESCRIPTION ──────────────────────────────
    doc.add_heading('5. Dataset Description', level=1)
    doc.add_paragraph(
        "The dataset is sourced from the Kaggle Supermarket Sales dataset by Aung Pyae "
        "(https://www.kaggle.com/datasets/aungpyaeap/supermarket-sales). It contains "
        f"{metrics['total_transactions']:,} sales transactions from three supermarket branches "
        "in Myanmar (Yangon, Mandalay, Naypyitaw) recorded between January and March 2019."
    )

    doc.add_heading('Dataset Summary', level=2)
    summary_data = pd.DataFrame({
        'Attribute': ['Records', 'Columns', 'Time Period', 'Branches', 'Product Lines',
                      'Customer Types', 'Payment Methods'],
        'Value': ['1,000', '17', 'Jan–Mar 2019', '3 (A, B, C)',
                  '6', '2 (Member, Normal)', '3 (Cash, Ewallet, Credit card)']
    })
    add_table_from_df(doc, summary_data)

    # ── 6. TOOLS AND TECHNOLOGIES ───────────────────────────
    doc.add_heading('6. Tools and Technologies', level=1)
    tools = pd.DataFrame({
        'Tool': ['Python 3.9+', 'Pandas', 'NumPy', 'Matplotlib', 'Seaborn',
                 'Scikit-learn', 'Jupyter Notebook', 'python-docx', 'Pytest'],
        'Purpose': ['Primary programming language', 'Data manipulation & analysis',
                     'Numerical operations', 'Visualization', 'Statistical visualization',
                     'Machine learning', 'Interactive notebook', 'Report generation',
                     'Unit testing']
    })
    add_table_from_df(doc, tools)

    # ── 7. METHODOLOGY ──────────────────────────────────────
    doc.add_heading('7. Methodology', level=1)
    doc.add_paragraph(
        "The project follows a structured data analytics workflow:"
    )
    methodology_steps = [
        "Data Collection: Obtained the publicly available Kaggle dataset",
        "Data Quality Assessment: Schema validation, missing values, duplicates, type checks",
        "Data Cleaning: Column standardization, date/time parsing, type conversions",
        "Exploratory Data Analysis: Descriptive statistics, group comparisons, temporal trends",
        "Visualization: Professional charts for all key dimensions",
        "Machine Learning: Random Forest regression with baseline comparison",
        "Insight Generation: Evidence-based findings with recommendations and limitations"
    ]
    for i, step in enumerate(methodology_steps, 1):
        doc.add_paragraph(f"{i}. {step}")

    # ── 8. DATA CLEANING ────────────────────────────────────
    doc.add_heading('8. Data Cleaning and Preprocessing', level=1)

    doc.add_paragraph(
        f"The raw dataset contained {cleaning_report['original_shape'][0]} rows and "
        f"{cleaning_report['original_shape'][1]} columns."
    )

    doc.add_heading('Cleaning Steps Performed', level=2)
    cleaning_steps = [
        f"Column name standardization (whitespace trimming)",
        f"Duplicate detection: {cleaning_report['duplicates_removed']} duplicates removed",
        "Date column parsed to datetime; extracted Day, Month, Month_Name, Day_of_Week, Week_Number",
        "Time column parsed; extracted Hour",
        "Numeric columns validated and coerced to proper types",
        "Categorical values validated against expected categories",
    ]
    for step in cleaning_steps:
        doc.add_paragraph(step, style='List Bullet')

    if cleaning_report['missing_values'].empty:
        doc.add_paragraph("Missing Values: No missing values were found in the dataset.")
    else:
        doc.add_paragraph("Missing Values:")
        add_table_from_df(doc, cleaning_report['missing_values'].reset_index())

    if not cleaning_report['numerical_issues']:
        doc.add_paragraph(
            "Numerical Validation: All numerical values are within expected ranges."
        )

    doc.add_paragraph(
        f"Final cleaned dataset: {cleaning_report['final_shape'][0]} rows × "
        f"{cleaning_report['final_shape'][1]} columns (including derived features)."
    )

    # ── 9. EXPLORATORY DATA ANALYSIS ────────────────────────
    doc.add_heading('9. Exploratory Data Analysis', level=1)

    # 9.1 Overall Metrics
    doc.add_heading('9.1 Overall Performance', level=2)
    metrics_df = pd.DataFrame([
        ('Total Transactions', f"{metrics['total_transactions']:,}"),
        ('Total Sales', f"${metrics.get('total_sales', 0):,.2f}"),
        ('Average Transaction', f"${metrics.get('average_transaction', 0):,.2f}"),
        ('Median Transaction', f"${metrics.get('median_transaction', 0):,.2f}"),
        ('Total Quantity Sold', f"{metrics.get('total_quantity', 0):,}"),
        ('Total Gross Income', f"${metrics.get('total_gross_income', 0):,.2f}"),
        ('Average Rating', f"{metrics.get('avg_rating', 0):.2f} / 10"),
    ], columns=['Metric', 'Value'])
    add_table_from_df(doc, metrics_df, 'Table: Key Performance Indicators')

    # 9.2 Product Line
    doc.add_heading('9.2 Product Line Analysis', level=2)
    if 'sales_by_product' in pl_results:
        add_table_from_df(doc, pl_results['sales_by_product'],
                          'Table: Total Sales by Product Line')
        add_figure(doc, os.path.join(FIGURES, 'sales_by_product_line.png'),
                   'Figure: Total Sales by Product Line')
        add_figure(doc, os.path.join(FIGURES, 'txn_count_by_product_line.png'),
                   'Figure: Transaction Count by Product Line')

    # 9.3 Branch
    doc.add_heading('9.3 Branch Analysis', level=2)
    if 'sales_by_branch' in br_results:
        add_table_from_df(doc, br_results['sales_by_branch'],
                          'Table: Total Sales by Branch')
        add_figure(doc, os.path.join(FIGURES, 'sales_by_branch.png'),
                   'Figure: Branch Performance Comparison')

    # 9.4 Customer
    doc.add_heading('9.4 Customer Analysis', level=2)
    if 'sales_by_customer_type' in cust_results:
        add_table_from_df(doc, cust_results['sales_by_customer_type'],
                          'Table: Sales by Customer Type')
        add_figure(doc, os.path.join(FIGURES, 'customer_analysis.png'),
                   'Figure: Customer Segment Analysis')

    # 9.5 Payment
    doc.add_heading('9.5 Payment Method Analysis', level=2)
    if 'sales_by_payment' in pay_results:
        add_table_from_df(doc, pay_results['sales_by_payment'],
                          'Table: Sales by Payment Method')
        add_figure(doc, os.path.join(FIGURES, 'payment_analysis.png'),
                   'Figure: Payment Method Analysis')

    # 9.6 Temporal
    doc.add_heading('9.6 Temporal Analysis', level=2)
    add_figure(doc, os.path.join(FIGURES, 'daily_sales_trend.png'),
               'Figure: Daily Sales Trend')
    add_figure(doc, os.path.join(FIGURES, 'monthly_sales.png'),
               'Figure: Monthly Sales Performance')
    add_figure(doc, os.path.join(FIGURES, 'day_of_week_sales.png'),
               'Figure: Sales by Day of Week')
    add_figure(doc, os.path.join(FIGURES, 'hourly_sales.png'),
               'Figure: Hourly Sales Distribution')

    # 9.7 Ratings
    doc.add_heading('9.7 Customer Rating Analysis', level=2)
    if 'rating_stats' in rate_results:
        rating_df = pd.DataFrame([
            ('Mean', rate_results['rating_stats']['mean']),
            ('Median', rate_results['rating_stats']['median']),
            ('Std Dev', rate_results['rating_stats']['std']),
            ('Min', rate_results['rating_stats']['min']),
            ('Max', rate_results['rating_stats']['max']),
        ], columns=['Statistic', 'Value'])
        add_table_from_df(doc, rating_df, 'Table: Rating Statistics')

    add_figure(doc, os.path.join(FIGURES, 'rating_distribution.png'),
               'Figure: Customer Rating Distribution')
    add_figure(doc, os.path.join(FIGURES, 'rating_by_product_line.png'),
               'Figure: Rating by Product Line')

    # 9.8 Correlation
    doc.add_heading('9.8 Correlation Analysis', level=2)
    add_figure(doc, os.path.join(FIGURES, 'correlation_heatmap.png'),
               'Figure: Correlation Heatmap')
    doc.add_paragraph(
        "Note: High correlations between Total, cogs, Tax 5%, and gross income are expected "
        "because they are mathematically derived from each other (Total = cogs × 1.05). "
        "These correlations are trivial and do not represent independently discovered patterns."
    )

    # 9.9 Distribution
    add_figure(doc, os.path.join(FIGURES, 'sales_distribution.png'),
               'Figure: Distribution of Transaction Values')

    # ── 10. MACHINE LEARNING ────────────────────────────────
    doc.add_heading('10. Machine Learning Model', level=1)

    doc.add_heading('10.1 Approach', level=2)
    doc.add_paragraph(
        "A Random Forest Regressor was trained to predict transaction Total from product "
        "and transaction attributes. Features excluded: Tax 5%, cogs, gross income "
        "(to avoid target leakage, as these are mathematically derived from Total)."
    )

    doc.add_heading('10.2 Important Caveat', level=2)
    doc.add_paragraph(
        "Total = Unit price × Quantity × 1.05. Since Unit price and Quantity are included "
        "as features, the model is learning a near-deterministic relationship. This section "
        "demonstrates the ML pipeline methodology rather than genuine predictive modeling."
    )

    add_figure(doc, os.path.join(FIGURES, 'feature_importance.png'),
               'Figure: Feature Importance — Random Forest')
    add_figure(doc, os.path.join(FIGURES, 'actual_vs_predicted.png'),
               'Figure: Actual vs Predicted Values')

    # ── 11. RESULTS AND FINDINGS ────────────────────────────
    doc.add_heading('11. Results and Findings', level=1)

    for i, insight in enumerate(insights, 1):
        doc.add_heading(f'Finding {i}: {insight["category"]}', level=2)
        doc.add_paragraph(f'Observation: {insight["finding"]}')
        doc.add_paragraph(f'Key Metric: {insight["metric"]}')
        doc.add_paragraph(f'Recommendation: {insight["recommendation"]}')
        doc.add_paragraph(f'Limitation: {insight["limitation"]}')

    # ── 12. BUSINESS RECOMMENDATIONS ────────────────────────
    doc.add_heading('12. Business Recommendations', level=1)
    recommendations = [
        "Optimize inventory for top-performing product lines while investigating "
        "underperforming categories for improvement opportunities.",
        "Implement branch-level best practices from the highest-performing branch "
        "across all locations.",
        "Strengthen the membership program with exclusive benefits to convert "
        "Normal customers to Members.",
        "Ensure seamless checkout across all payment methods; consider e-wallet "
        "promotions to drive digital adoption.",
        "Align staffing levels with peak sales hours to maximize service quality "
        "during high-traffic periods.",
        "Conduct targeted customer satisfaction surveys to understand drivers of "
        "lower ratings and implement improvements.",
        "Expand data collection to enable longitudinal analysis and customer "
        "lifetime value tracking."
    ]
    for rec in recommendations:
        doc.add_paragraph(rec, style='List Bullet')

    # ── 13. LIMITATIONS ─────────────────────────────────────
    doc.add_heading('13. Limitations', level=1)
    limitations = [
        "Limited 3-month time window prevents seasonal and long-term trend analysis.",
        "All branches are in Myanmar, limiting geographic generalizability.",
        "No customer-level tracking for repeat purchase or lifetime value analysis.",
        "Constant gross margin percentage limits profitability analysis depth.",
        "Self-reported ratings may not reflect long-term customer satisfaction.",
        "ML model learns a deterministic formula, not genuine prediction.",
        "Observed correlations do not establish causal relationships."
    ]
    for lim in limitations:
        doc.add_paragraph(lim, style='List Bullet')

    # ── 14. CONCLUSION ──────────────────────────────────────
    doc.add_heading('14. Conclusion', level=1)
    doc.add_paragraph(
        f"This project successfully analyzed {metrics['total_transactions']:,} supermarket "
        f"sales transactions totaling ${metrics.get('total_sales', 0):,.2f} across three "
        f"branches. The comprehensive exploratory data analysis revealed meaningful patterns "
        f"in product performance, branch operations, customer behavior, and temporal trends. "
        f"Professional visualizations effectively communicated key findings, and a machine "
        f"learning pipeline was demonstrated with appropriate caveats. The evidence-based "
        f"insights and recommendations provide actionable guidance for supermarket management "
        f"to optimize revenue, improve customer experience, and make data-driven decisions."
    )

    # ── 15. REFERENCES ──────────────────────────────────────
    doc.add_heading('15. References', level=1)
    references = [
        'Aung Pyae, "Supermarket Sales" dataset, Kaggle (2019). '
        'https://www.kaggle.com/datasets/aungpyaeap/supermarket-sales',
        'McKinney, W. "pandas: a foundational Python library for data analysis and statistics." '
        'Python for High Performance and Scientific Computing (2011).',
        'Pedregosa, F., et al. "Scikit-learn: Machine Learning in Python." '
        'JMLR 12 (2011): 2825-2830.',
        'Hunter, J.D. "Matplotlib: A 2D Graphics Environment." '
        'Computing in Science & Engineering (2007).',
        'Waskom, M. "seaborn: statistical data visualization." '
        'Journal of Open Source Software (2021).',
    ]
    for i, ref in enumerate(references, 1):
        doc.add_paragraph(f'[{i}] {ref}')

    # ── Add page numbers (via section footer) ───────────────
    for section in doc.sections:
        section.top_margin = Cm(2.54)
        section.bottom_margin = Cm(2.54)
        section.left_margin = Cm(2.54)
        section.right_margin = Cm(2.54)

    # Save
    output_path = 'AtharavTayade_ProjectReport.docx'
    doc.save(output_path)
    print(f'[OK] Report saved to: {output_path}')
    print(f'   File size: {os.path.getsize(output_path) / 1024:.1f} KB')
    return output_path


if __name__ == '__main__':
    generate_report()
