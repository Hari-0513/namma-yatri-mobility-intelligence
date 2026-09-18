# Bengaluru Mobility Intelligence

### Namma Yatri Ride Analytics, Demand & Operational Performance

An end-to-end **Data Analytics / Business Intelligence portfolio project** analyzing Namma Yatri mobility activity across Bengaluru wards using **Python, Microsoft SQL Server, Power BI, and statistical/predictive analysis where justified by the data**.

---

##  Project Objective

### Main Business Question

> **How does ride-hailing demand behave across Bengaluru, what factors are associated with operational performance, and how can data support better mobility decisions?**

The project follows this workflow:

```text
Raw Data
   ↓
Validation
   ↓
Python Cleaning & EDA
   ↓
SQL Server Analysis
   ↓
Power BI Data Model & Dashboard
   ↓
Statistical / Predictive Analysis
   ↓
Business Insights & Recommendations
```

The focus is on **practical analytics and business reasoning**, rather than adding technology that the problem does not require.

---

##  Dataset

### Primary Dataset

**Namma Yatri Cab Bookings Bangalore Open Data — Kaggle**

The available dataset is **ward-level aggregated data**, not individual ride-level data.

### Dataset Profile

* **245 rows**
* **244 actual Bengaluru wards**
* **1 `Bangalore Total` aggregate row**
* **18 columns**
* No missing values identified during validation
* No duplicate rows identified during validation

### Available Information

The dataset contains measures covering:

* Searches
* Estimates and quote searches
* Quotes
* Bookings
* Completed trips
* Cancelled bookings
* Conversion/funnel rates
* Driver earnings
* Average trip distance
* Average fare
* Total distance travelled
* Ward-level geography

### Important Data Limitation

The current dataset does **not** contain:

* Individual ride records
* Date/time fields
* Pickup coordinates
* Destination coordinates
* Trip duration
* Service type

Therefore, the project does **not** claim to analyze hourly/weekly seasonality, routes, trip duration, or time-series demand forecasting from this dataset.

The scope is deliberately restricted to analyses supported by the available data.

---

#  Technology Stack

| Technology               | Purpose                                                             |
| ------------------------ | ------------------------------------------------------------------- |
| **Python**               | Cleaning, EDA, statistics, feature engineering, predictive analysis |
| **Pandas / NumPy**       | Data manipulation and numerical analysis                            |
| **Matplotlib / Seaborn** | Exploratory visualization                                           |
| **scikit-learn**         | Predictive modeling where justified                                 |
| **Microsoft SQL Server** | Data storage and analytical SQL                                     |
| **Power BI**             | Data modeling, DAX, dashboards and business reporting               |
| **Git / GitHub**         | Version control and project documentation                           |
| **VS Code / Jupyter**    | Development and analysis                                            |

---

# 📁 Project Structure

```text
Bengaluru-Mobility-Intelligence/
│
├── data/
│   ├── raw/
│   │   └── All-time Table-Bangalore-Wards.csv
│   │
│   └── processed/
│       ├── namma_yatri_bengaluru_cleaned.csv
│       └── day03_ward_demand_summary.csv
│
├── python/
│   ├── day01_dataset_validation.py
│   ├── day02_data_cleaning.py
│   └── day03_demand_eda.py
│
├── sql/
│   └── ...
│
├── powerbi/
│   └── ...
│
├── reports/
│   ├── day01_dataset_validation.txt
│   ├── day02_data_cleaning.txt
│   ├── day03_demand_eda.txt
│   └── figures/
│
├── README.md
└── .gitignore
```

The structure will expand as additional project stages are completed.

---

#  Project Progress

## Day 1 — Dataset Validation ✅

Validated the raw dataset before modifying or analyzing it.

### Checks performed

* File existence
* Dataset dimensions
* Column names
* Data types
* Missing values
* Duplicate rows
* Unique wards
* Aggregate total row
* Date/time availability
* Numeric and percentage fields stored as text

### Key findings

* 245 rows were present.
* 244 rows represent actual wards.
* `Bangalore Total` is an aggregate city-level row.
* No missing values were identified.
* No duplicate rows were identified.
* Several numerical and percentage fields required type conversion.
* No date/time field is available.

---

## Day 2 — Data Cleaning ✅

Created a separate cleaned dataset while preserving the raw source.

### Work completed

* Standardized column names
* Removed currency symbols and thousands separators
* Converted numeric columns to numeric data types
* Converted percentage columns to numeric values
* Removed unnecessary whitespace
* Added an aggregate-row indicator
* Validated conversion results
* Saved cleaned data separately

Output:

```text
data/processed/namma_yatri_bengaluru_cleaned.csv
```

---

## Day 3 — Demand EDA ✅

Analyzed the distribution and concentration of platform activity across the 244 actual wards.

### Current totals

| Metric          |      Total |
| --------------- | ---------: |
| Searches        | 67,334,064 |
| Bookings        | 29,453,513 |
| Completed Trips | 18,628,581 |

### Demand concentration

The top 10 wards account for approximately:

* **23.16% of searches**
* **19.31% of bookings**
* **18.43% of completed trips**

### Relationships

| Relationship               | Correlation |
| -------------------------- | ----------: |
| Searches ↔ Bookings        |  **0.9792** |
| Searches ↔ Completed Trips |  **0.9654** |

These values indicate strong positive associations in the dataset. They are **not interpreted as causal relationships**.

### Visual analysis

Day 3 also produced:

* Top wards by searches
* Top wards by bookings
* Top wards by completed trips
* Searches vs. bookings scatter plot
* Ward-level demand summary

---

#  Planned Power BI Dashboard

The final report is planned around four pages.

## Page 1 — Executive Overview

High-level KPIs and business summary.

Potential metrics include:

* Searches
* Bookings
* Completed trips
* Cancellations
* Conversion
* Driver earnings
* Distance/fare indicators

Final KPIs will be locked after the analytical model is complete.

## Page 2 — Demand & Geography

Focus:

* Ward-level demand
* Top/bottom wards
* Demand concentration
* Searches vs. bookings
* Searches vs. completed trips
* Geographic comparisons supported by the dataset

## Page 3 — Fare & Operations

Focus:

* Completed trips
* Cancellation behavior
* Average fare
* Average distance
* Driver earnings
* Operational relationships

## Page 4 — Advanced Insights

The final content will depend on what the data supports.

Possible areas:

* Statistical analysis
* Ward segmentation
* Derived performance indicators
* Predictive analysis

---

#  Predictive Analytics

Machine learning is an **optional analytical layer**, not a requirement.

A predictive problem will only be included if the available dataset provides:

1. A meaningful target variable
2. Sufficient observations
3. Appropriate predictors
4. A defensible business use case
5. A measurable evaluation approach

If these conditions are not met, the project will prioritize deeper statistical and business analysis instead of forcing an ML model into the project.

---

#  Business Questions

The project is designed to investigate questions such as:

1. Where is Namma Yatri activity concentrated across Bengaluru?
2. Which wards generate the highest search and booking volumes?
3. How does search activity translate into bookings and completed trips?
4. Where are cancellation rates relatively high?
5. How do fare and distance vary across wards?
6. How does driver earnings relate to trip activity?
7. Which wards combine high demand with different levels of funnel efficiency?
8. What operational patterns can be identified?
9. What data-driven actions could support mobility planning and operational decision-making?

---

#  Analytical Approach

### Data First

Variables and analyses are not assumed to exist before the dataset is inspected.

### Evidence Over Assumptions

Business findings are based on measurable patterns in the available data.

### Correlation ≠ Causation

Relationships are reported as associations unless causal evidence is available.

### ML Only When Justified

A model must solve a meaningful analytical problem; it will not be added simply to make the project look more advanced.

### Business Value Over Unnecessary Complexity

The project prioritizes:

```text
Python
+
SQL
+
Power BI
+
Statistics
+
Business Reasoning
```

over unnecessary technologies.

---

#  Skills Demonstrated

This project demonstrates practical experience in:

* Data validation
* Data cleaning
* Exploratory data analysis
* Data quality assessment
* Statistical reasoning
* Feature engineering
* SQL
* Microsoft SQL Server
* Power BI
* DAX
* Data visualization
* Business analysis
* Predictive analytics
* Insight generation
* Business recommendations
* Git/GitHub
* End-to-end analytics workflow

---

#  Planned Final Deliverables

By completion, the repository is intended to contain:

* Validated raw-data documentation
* Cleaned dataset
* Python analysis scripts
* EDA visualizations
* SQL Server database/scripts
* Business SQL queries
* Power BI dashboard
* DAX measures
* Statistical analysis
* Predictive analysis if justified
* Business insights
* Recommendations
* Project documentation
* Reproducible Git history

---

#  Data & Scope Disclaimer

This is a portfolio analysis using an available public/third-party dataset.

It does **not** claim access to:

* Namma Yatri internal systems
* Proprietary company data
* Real-time operational data
* Private customer information
* Private driver information
* Internal company decisions

All findings are interpreted within the scope and limitations of the dataset used.

---

# 📌 Project Positioning

**Bengaluru Mobility Intelligence** demonstrates how an available mobility dataset can be transformed through:

```text
DATA
  ↓
CLEANING
  ↓
EXPLORATION
  ↓
SQL ANALYSIS
  ↓
BI / VISUALIZATION
  ↓
STATISTICS / ML
  ↓
BUSINESS INSIGHT
  ↓
DECISION SUPPORT
```

The project is built to demonstrate **real analytical thinking, reproducibility, technical skills, and business relevance** rather than simply showcasing tools.
