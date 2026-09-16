"""
Bengaluru Mobility Intelligence
Day 01 - Dataset Validation

Purpose:
    Validate the raw Namma Yatri Bengaluru ward-level dataset before
    cleaning, SQL loading, or Power BI development.

Input:
    data/raw/All-time Table-Bangalore-Wards.csv

Output:
    reports/day01_dataset_validation.txt

Important:
    This script DOES NOT modify the raw dataset.
"""

from pathlib import Path
import pandas as pd


# ---------------------------------------------------------------------
# 1. PROJECT PATHS
# ---------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_FILE = PROJECT_ROOT / "data" / "raw" / "All-time Table-Bangalore-Wards.csv"
REPORT_FILE = PROJECT_ROOT / "reports" / "day01_dataset_validation.txt"


# ---------------------------------------------------------------------
# 2. LOAD RAW DATA
# ---------------------------------------------------------------------

if not RAW_FILE.exists():
    raise FileNotFoundError(
        f"Raw dataset not found:\n{RAW_FILE}\n\n"
        "Place the CSV inside the project's data/raw folder."
    )

df = pd.read_csv(RAW_FILE)


# ---------------------------------------------------------------------
# 3. BASIC DATASET INFORMATION
# ---------------------------------------------------------------------

row_count, column_count = df.shape

columns = df.columns.tolist()
data_types = df.dtypes.astype(str)

missing_values = df.isna().sum()
total_missing_values = int(missing_values.sum())

duplicate_rows = int(df.duplicated().sum())

ward_count = int(df["Ward"].nunique())

total_row_mask = (
    df["Ward"]
    .astype(str)
    .str.strip()
    .str.lower()
    .eq("bangalore total")
)

total_row_count = int(total_row_mask.sum())
actual_ward_count = ward_count - total_row_count


# ---------------------------------------------------------------------
# 4. NUMERIC-TYPE CHECK
# ---------------------------------------------------------------------

numeric_columns = [
    "Searches",
    "Searches which got estimate",
    "Searches for Quotes",
    "Searches which got Quotes",
    "Bookings",
    "Completed Trips",
    "Cancelled Bookings",
    "Drivers' Earnings",
    "Average Fare per Trip",
    "Distance Travelled (km)",
]

percentage_columns = [
    "Search-to-estimate Rate",
    "Estimate-to-search for quotes Rate",
    "Quote Acceptance Rate",
    "Quote-to-booking Rate",
    "Booking Cancellation Rate",
    "Conversion Rate",
]

numeric_columns_stored_as_object = [
    column
    for column in numeric_columns
    if column in df.columns and not pd.api.types.is_numeric_dtype(df[column])
]

percentage_columns_stored_as_object = [
    column
    for column in percentage_columns
    if column in df.columns and not pd.api.types.is_numeric_dtype(df[column])
]


# ---------------------------------------------------------------------
# 5. DATASET PERIOD / TIME CHECK
# ---------------------------------------------------------------------

date_columns = []

# Only inspect columns whose names suggest a date/time field.
# This avoids falsely interpreting ordinary numeric values as dates.
for column in df.columns:
    column_name = str(column).lower()
    if any(keyword in column_name for keyword in ["date", "time", "timestamp"]):
        parsed = pd.to_datetime(df[column], errors="coerce")
        if parsed.notna().mean() >= 0.80:
            date_columns.append(column)


# ---------------------------------------------------------------------
# 6. GENERATE VALIDATION REPORT
# ---------------------------------------------------------------------

report_lines = []

report_lines.append("BENGALURU MOBILITY INTELLIGENCE")
report_lines.append("DAY 01 - DATASET VALIDATION REPORT")
report_lines.append("=" * 60)
report_lines.append("")

report_lines.append("1. FILE")
report_lines.append("-" * 60)
report_lines.append(f"Input file: {RAW_FILE.name}")
report_lines.append("")

report_lines.append("2. DATASET SIZE")
report_lines.append("-" * 60)
report_lines.append(f"Rows: {row_count}")
report_lines.append(f"Columns: {column_count}")
report_lines.append("")

report_lines.append("3. COLUMN NAMES AND DATA TYPES")
report_lines.append("-" * 60)
for column in columns:
    report_lines.append(f"{column} -> {data_types[column]}")
report_lines.append("")

report_lines.append("4. MISSING VALUES")
report_lines.append("-" * 60)
report_lines.append(f"Total missing values: {total_missing_values}")

for column, count in missing_values.items():
    if count > 0:
        report_lines.append(f"{column}: {count}")
report_lines.append("")

report_lines.append("5. DUPLICATES")
report_lines.append("-" * 60)
report_lines.append(f"Duplicate rows: {duplicate_rows}")
report_lines.append("")

report_lines.append("6. WARD CHECK")
report_lines.append("-" * 60)
report_lines.append(f"Unique Ward values: {ward_count}")
report_lines.append(f"Overall total rows: {total_row_count}")
report_lines.append(f"Actual ward rows: {actual_ward_count}")
report_lines.append("Overall total label detected: Bangalore Total")
report_lines.append("")

report_lines.append("7. NUMERIC COLUMNS CURRENTLY STORED AS TEXT")
report_lines.append("-" * 60)
if numeric_columns_stored_as_object:
    for column in numeric_columns_stored_as_object:
        report_lines.append(column)
else:
    report_lines.append("None")
report_lines.append("")

report_lines.append("8. PERCENTAGE COLUMNS CURRENTLY STORED AS TEXT")
report_lines.append("-" * 60)
if percentage_columns_stored_as_object:
    for column in percentage_columns_stored_as_object:
        report_lines.append(column)
else:
    report_lines.append("None")
report_lines.append("")

report_lines.append("9. DATE/TIME CHECK")
report_lines.append("-" * 60)
if date_columns:
    report_lines.append("Potential date/time columns:")
    for column in date_columns:
        report_lines.append(column)
else:
    report_lines.append("No date/time column detected.")
report_lines.append("")

report_lines.append("10. VALIDATION SUMMARY")
report_lines.append("-" * 60)
report_lines.append("Raw dataset loaded successfully: YES")
report_lines.append("Raw dataset modified: NO")
report_lines.append(f"Missing values: {total_missing_values}")
report_lines.append(f"Duplicate rows: {duplicate_rows}")
report_lines.append(f"Actual ward records: {actual_ward_count}")
report_lines.append("Dataset granularity: Ward-level aggregate")
report_lines.append("")

report_lines.append("11. DAY 01 CONCLUSION")
report_lines.append("-" * 60)
report_lines.append(
    "The dataset is suitable for ward-level demand, booking-funnel, "
    "operational, geographic, distance, fare, and driver-earnings analysis."
)
report_lines.append(
    "The dataset does not contain a usable ride-level date/time field, "
    "so hourly/daily time-series analysis and demand forecasting should "
    "not be assumed."
)
report_lines.append(
    "Numeric, currency, and percentage fields stored as text will be "
    "handled during Day 02 data cleaning."
)

REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
REPORT_FILE.write_text("\n".join(report_lines), encoding="utf-8")

print("\n".join(report_lines))
print(f"\nValidation report saved to: {REPORT_FILE}")
