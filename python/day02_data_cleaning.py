from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = PROJECT_ROOT / "data" / "raw" / "All-time Table-Bangalore-Wards.csv"
CLEAN_FILE = PROJECT_ROOT / "data" / "processed" / "namma_yatri_bengaluru_cleaned.csv"
REPORT_FILE = PROJECT_ROOT / "reports" / "day02_data_cleaning.txt"

if not RAW_FILE.exists():
    raise FileNotFoundError(f"Raw dataset not found: {RAW_FILE}")

df = pd.read_csv(RAW_FILE)
original_shape = df.shape
df = df.rename(columns={
    "Searches which got estimate": "Searches_Got_Estimate",
    "Searches for Quotes": "Searches_For_Quotes",
    "Searches which got Quotes": "Searches_Got_Quotes",
    "Completed Trips": "Completed_Trips",
    "Search-to-estimate Rate": "Search_To_Estimate_Rate",
    "Estimate-to-search for quotes Rate": "Estimate_To_Quote_Search_Rate",
    "Quote Acceptance Rate": "Quote_Acceptance_Rate",
    "Quote-to-booking Rate": "Quote_To_Booking_Rate",
    "Cancelled Bookings": "Cancelled_Bookings",
    "Booking Cancellation Rate": "Booking_Cancellation_Rate",
    "Conversion Rate": "Conversion_Rate",
    "Drivers' Earnings": "Drivers_Earnings",
    "Average Distance per Trip (km)": "Average_Distance_Per_Trip_Km",
    "Average Fare per Trip": "Average_Fare_Per_Trip",
    "Distance Travelled (km)": "Distance_Travelled_Km",
})

df["Ward"] = df["Ward"].astype(str).str.strip()
df["Is_Bangalore_Total"] = df["Ward"].str.lower().eq("bangalore total")

numeric_columns = [
    "Searches", "Searches_Got_Estimate", "Searches_For_Quotes",
    "Searches_Got_Quotes", "Bookings", "Completed_Trips",
    "Cancelled_Bookings", "Drivers_Earnings", "Average_Distance_Per_Trip_Km",
    "Average_Fare_Per_Trip", "Distance_Travelled_Km",
]
percentage_columns = [
    "Search_To_Estimate_Rate", "Estimate_To_Quote_Search_Rate",
    "Quote_Acceptance_Rate", "Quote_To_Booking_Rate",
    "Booking_Cancellation_Rate", "Conversion_Rate",
]
for col in numeric_columns:
    df[col] = (df[col].astype(str)
               .str.replace(",", "", regex=False)
               .str.replace("₹", "", regex=False)
               .str.strip())
    df[col] = pd.to_numeric(df[col], errors="coerce")

for col in percentage_columns:
    df[col] = pd.to_numeric(
        df[col].astype(str).str.replace("%", "", regex=False).str.strip(),
        errors="coerce"
    )

numeric_errors = int(df[numeric_columns].isna().sum().sum())
percentage_errors = int(df[percentage_columns].isna().sum().sum())
duplicates = int(df.duplicated().sum())

CLEAN_FILE.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(CLEAN_FILE, index=False)

report = f"""BENGALURU MOBILITY INTELLIGENCE
DAY 02 - DATA CLEANING REPORT
============================================================

Original shape: {original_shape[0]} rows x {original_shape[1]} columns
Cleaned shape:  {df.shape[0]} rows x {df.shape[1]} columns

Cleaning performed:
- Standardized column names.
- Removed leading/trailing whitespace from Ward values.
- Added Is_Bangalore_Total to identify the city-total row.
- Converted comma-formatted counts to numeric values.
- Removed ₹ and comma formatting from monetary fields and converted them to numeric.
- Removed % signs from rate fields and converted them to numeric percentage points.
- Preserved the raw CSV unchanged.

Validation:
- Numeric conversion errors: {numeric_errors}
- Percentage conversion errors: {percentage_errors}
- Duplicate rows after cleaning: {duplicates}
- Bangalore Total rows: {int(df['Is_Bangalore_Total'].sum())}

Output:
{CLEAN_FILE}
"""
REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
REPORT_FILE.write_text(report, encoding="utf-8")
print(report)
